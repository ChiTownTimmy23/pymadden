"""Async client for the EA Madden NFL ratings APIs.

Supports the legacy API (Madden 22-24) and the drop API (Madden 25) behind a
single interface, with connection reuse, concurrent pagination, retries with
exponential backoff, client-side rate limiting, and TTL response caching.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from typing import Any

import httpx

from .config import Config, GameVersion, Iteration, M25Iteration, validate_iteration
from .exceptions import (
    MaddenAPIError,
    MaddenConnectionError,
    MaddenRateLimitError,
    MaddenValidationError,
)
from .models import M25Player, M25RatingsResponse, PlayerRating, RatingsResponse

logger = logging.getLogger("pymadden")

Player = PlayerRating | M25Player
IterationLike = str | Iteration | M25Iteration


class _RateLimiter:
    """Enforces a minimum interval between outgoing requests."""

    def __init__(self, requests_per_second: float):
        self._interval = 1.0 / requests_per_second if requests_per_second > 0 else 0.0
        self._lock = asyncio.Lock()
        self._next_allowed = 0.0

    async def acquire(self) -> None:
        if self._interval <= 0:
            return
        async with self._lock:
            now = time.monotonic()
            wait = self._next_allowed - now
            self._next_allowed = max(now, self._next_allowed) + self._interval
        if wait > 0:
            await asyncio.sleep(wait)


class MaddenAPI:
    """Client for the EA Madden ratings APIs.

    Usage::

        async with MaddenAPI("m24") as api:
            players = await api.get_players(Iteration.WEEK_1)

    Or without a context manager (a client is created per call batch)::

        api = MaddenAPI("m25")
        players = await api.get_players()

    :param game_version: One of "m22", "m23", "m24", "m25" (or a GameVersion).
    :param timeout: Per-request timeout in seconds.
    :param max_retries: Retry attempts for transient failures (5xx, 429, network).
    :param max_concurrency: Max in-flight page requests during pagination.
    :param requests_per_second: Client-side rate limit (0 disables).
    :param cache_ttl: Seconds to cache full-iteration results (0 disables).
    """

    def __init__(
        self,
        game_version: str | GameVersion = "m24",
        *,
        timeout: float = Config.DEFAULT_TIMEOUT,
        max_retries: int = Config.DEFAULT_MAX_RETRIES,
        max_concurrency: int = Config.DEFAULT_MAX_CONCURRENCY,
        requests_per_second: float = Config.DEFAULT_REQUESTS_PER_SECOND,
        cache_ttl: float = Config.DEFAULT_CACHE_TTL,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.game_version = GameVersion.parse(game_version)
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_concurrency = max_concurrency
        self.cache_ttl = cache_ttl
        self._transport = transport
        self._backoff_base = 1.0
        self._rate_limiter = _RateLimiter(requests_per_second)
        self._cache: dict[str, tuple[float, list[Player]]] = {}
        self._client: httpx.AsyncClient | None = None

    # -- lifecycle -----------------------------------------------------------

    async def __aenter__(self) -> MaddenAPI:
        self._client = self._build_client()
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.close()

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _build_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            timeout=self.timeout,
            headers={"User-Agent": Config.USER_AGENT, "Accept": "application/json"},
            transport=self._transport,
        )

    # -- public API ----------------------------------------------------------

    async def get_players(self, iteration: IterationLike | None = None) -> list[Player]:
        """Retrieve all player ratings for an iteration (all pages).

        :param iteration: Ratings iteration; defaults to launch ratings.
        :return: ``List[PlayerRating]`` for m22-m24, ``List[M25Player]`` for m25.
        :raises ValueError: If the iteration is not valid for the game version.
        :raises MaddenAPIError: On HTTP errors from the API.
        :raises MaddenConnectionError: On network failures after retries.
        :raises MaddenValidationError: If the response shape is unexpected.
        """
        iteration_value = self._resolve_iteration(iteration)

        cached = self._cache_get(iteration_value)
        if cached is not None:
            logger.debug(
                "Cache hit for %s/%s", self.game_version.value, iteration_value
            )
            return cached

        started = time.monotonic()
        if self._client is not None:
            players = await self._fetch_all(self._client, iteration_value)
        else:
            async with self._build_client() as client:
                players = await self._fetch_all(client, iteration_value)
        logger.info(
            "Fetched %d players for %s/%s in %.2fs",
            len(players),
            self.game_version.value,
            iteration_value,
            time.monotonic() - started,
        )

        self._cache_put(iteration_value, players)
        return players

    def get_players_sync(self, iteration: IterationLike | None = None) -> list[Player]:
        """Synchronous convenience wrapper around :meth:`get_players`."""
        return asyncio.run(self.get_players(iteration))

    async def get_player_count(self, iteration: IterationLike | None = None) -> int:
        """Return the total player count for an iteration (single request)."""
        iteration_value = self._resolve_iteration(iteration)
        if self._client is not None:
            _, total = await self._fetch_page(self._client, iteration_value, offset=0)
        else:
            async with self._build_client() as client:
                _, total = await self._fetch_page(client, iteration_value, offset=0)
        return total

    def clear_cache(self) -> None:
        """Drop all cached responses."""
        self._cache.clear()

    # -- iteration / cache helpers -------------------------------------------

    def _resolve_iteration(self, iteration: IterationLike | None) -> str:
        if iteration is None:
            iteration = (
                M25Iteration.BASE
                if self.game_version is GameVersion.M25
                else Iteration.LAUNCH_RATINGS
            )
        return validate_iteration(self.game_version, iteration)

    def _cache_get(self, iteration_value: str) -> list[Player] | None:
        if self.cache_ttl <= 0:
            return None
        entry = self._cache.get(iteration_value)
        if entry is None:
            return None
        expires_at, players = entry
        if time.monotonic() >= expires_at:
            del self._cache[iteration_value]
            return None
        return players

    def _cache_put(self, iteration_value: str, players: list[Player]) -> None:
        if self.cache_ttl > 0:
            self._cache[iteration_value] = (
                time.monotonic() + self.cache_ttl,
                players,
            )

    # -- request plumbing ------------------------------------------------------

    def _page_url_and_params(
        self, iteration_value: str, offset: int
    ) -> tuple[str, dict[str, Any]]:
        if self.game_version.uses_legacy_api:
            path = Config.RATINGS_PATHS[self.game_version]
            url = f"{Config.BASE_URL}/{path}"
            params: dict[str, Any] = {
                "filter": f"iteration:{iteration_value}",
                "limit": Config.LEGACY_PAGE_SIZE,
                "offset": offset,
            }
        else:
            url = Config.M25_BASE_URL
            params = {
                "iteration": iteration_value,
                "locale": "en",
                "limit": Config.M25_PAGE_SIZE,
                "offset": offset,
            }
        return url, params

    @property
    def _page_size(self) -> int:
        return (
            Config.LEGACY_PAGE_SIZE
            if self.game_version.uses_legacy_api
            else Config.M25_PAGE_SIZE
        )

    async def _fetch_all(
        self, client: httpx.AsyncClient, iteration_value: str
    ) -> list[Player]:
        first_page, total = await self._fetch_page(client, iteration_value, offset=0)
        players: list[Player] = list(first_page)
        if total <= len(players):
            return players

        offsets = range(len(players), total, self._page_size)
        semaphore = asyncio.Semaphore(self.max_concurrency)

        async def fetch(offset: int) -> list[Player]:
            async with semaphore:
                page, _ = await self._fetch_page(client, iteration_value, offset)
                return page

        pages = await asyncio.gather(*(fetch(offset) for offset in offsets))
        for page in pages:
            players.extend(page)
        return players

    async def _fetch_page(
        self, client: httpx.AsyncClient, iteration_value: str, offset: int
    ) -> tuple[list[Player], int]:
        url, params = self._page_url_and_params(iteration_value, offset)
        data = await self._request_json(client, url, params)
        try:
            if self.game_version.uses_legacy_api:
                parsed = RatingsResponse(**data)
                return list(parsed.docs), parsed.count
            parsed_m25 = M25RatingsResponse(**data)
            return list(parsed_m25.items), parsed_m25.totalItems
        except (TypeError, ValueError) as exc:
            raise MaddenValidationError(
                f"Unexpected response shape from {url}: {exc}"
            ) from exc

    async def _request_json(
        self, client: httpx.AsyncClient, url: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            await self._rate_limiter.acquire()
            try:
                logger.debug("GET %s params=%s (attempt %d)", url, params, attempt + 1)
                response = await client.get(url, params=params)
            except httpx.HTTPError as exc:
                last_error = MaddenConnectionError(
                    f"Network error requesting {url}: {exc}"
                )
                await self._backoff(attempt, reason=str(exc))
                continue

            if response.status_code == 429:
                last_error = MaddenRateLimitError()
                await self._backoff(attempt, reason="HTTP 429")
                continue
            if response.status_code >= 500:
                last_error = MaddenAPIError(
                    f"Server error from {url}: HTTP {response.status_code}",
                    status_code=response.status_code,
                )
                await self._backoff(attempt, reason=f"HTTP {response.status_code}")
                continue
            if response.status_code >= 400:
                raise MaddenAPIError(
                    f"Client error from {url}: HTTP {response.status_code}",
                    status_code=response.status_code,
                )
            try:
                return response.json()
            except ValueError as exc:
                raise MaddenValidationError(f"Non-JSON response from {url}") from exc

        assert last_error is not None
        raise last_error

    async def _backoff(self, attempt: int, reason: str) -> None:
        if attempt >= self.max_retries:
            return
        delay = min(self._backoff_base * 2**attempt, 10)
        delay += random.uniform(0, delay * 0.25)
        logger.warning(
            "Request failed (%s); retrying in %.2fs (attempt %d/%d)",
            reason,
            delay,
            attempt + 1,
            self.max_retries,
        )
        await asyncio.sleep(delay)
