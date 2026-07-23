"""Tests for MaddenAPI using httpx.MockTransport (no real network)."""

import json

import httpx
import pytest

from pymadden.api import MaddenAPI
from pymadden.config import GameVersion, Iteration, M25Iteration
from pymadden.exceptions import MaddenAPIError, MaddenConnectionError
from pymadden.models import M25Player, PlayerRating

from .conftest import make_legacy_player, make_m25_player


def legacy_transport(players, page_size=1000):
    """MockTransport that serves legacy API documents with limit/offset."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        params = dict(request.url.params)
        offset = int(params.get("offset", 0))
        limit = int(params.get("limit", page_size))
        page = players[offset : offset + limit]
        return httpx.Response(200, json={"count": len(players), "docs": page})

    return httpx.MockTransport(handler), calls


def m25_transport(items):
    """MockTransport that serves drop API items with limit/offset."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        params = dict(request.url.params)
        offset = int(params.get("offset", 0))
        limit = int(params.get("limit", 100))
        page = items[offset : offset + limit]
        return httpx.Response(200, json={"items": page, "totalItems": len(items)})

    return httpx.MockTransport(handler), calls


def make_api(game, transport, **kwargs):
    kwargs.setdefault("requests_per_second", 0)
    kwargs.setdefault("cache_ttl", 0)
    kwargs.setdefault("max_retries", 0)
    return MaddenAPI(game, transport=transport, **kwargs)


async def test_get_players_legacy():
    players = [
        make_legacy_player(1, position="WR"),
        make_legacy_player(2, position="RB"),
    ]
    transport, _ = legacy_transport(players)
    api = make_api("m24", transport)

    result = await api.get_players()

    assert len(result) == 2
    assert all(isinstance(p, PlayerRating) for p in result)
    assert result[0].lastName == "Player1"
    assert result[0].position == "WR"
    assert result[1].position == "RB"


async def test_get_players_legacy_pagination():
    players = [make_legacy_player(i) for i in range(1, 2501)]
    transport, calls = legacy_transport(players)
    api = make_api("m22", transport)

    result = await api.get_players(Iteration.WEEK_1)

    assert len(result) == 2500
    assert {p.primaryKey for p in result} == set(range(1, 2501))
    assert len(calls) == 3  # 1000 + 1000 + 500
    assert all(c.url.params["filter"] == "iteration:week-1" for c in calls)


async def test_get_players_m25():
    items = [make_m25_player(1), make_m25_player(2, overallRating=99)]
    transport, calls = m25_transport(items)
    api = make_api("m25", transport)

    result = await api.get_players()

    assert len(result) == 2
    assert all(isinstance(p, M25Player) for p in result)
    assert result[1].overallRating == 99
    assert calls[0].url.host == "drop-api.ea.com"
    assert calls[0].url.params["iteration"] == "1-base"


async def test_get_players_m25_pagination():
    items = [make_m25_player(i) for i in range(1, 251)]
    transport, calls = m25_transport(items)
    api = make_api("m25", transport)

    result = await api.get_players(M25Iteration.WEEK_8)

    assert len(result) == 250
    assert {p.id for p in result} == set(range(1, 251))
    assert len(calls) == 3  # 100 + 100 + 50


async def test_iteration_accepts_string_and_enum():
    players = [make_legacy_player(1)]
    transport, calls = legacy_transport(players)
    api = make_api("m23", transport)

    await api.get_players("super-bowl")
    await api.get_players(Iteration.SUPER_BOWL)

    assert all(c.url.params["filter"] == "iteration:super-bowl" for c in calls)


async def test_invalid_game_version():
    with pytest.raises(ValueError, match="Invalid game version"):
        MaddenAPI(game_version="m99")


async def test_invalid_iteration():
    api = make_api("m24", httpx.MockTransport(lambda r: httpx.Response(200)))
    with pytest.raises(ValueError, match="Invalid iteration"):
        await api.get_players("week-20")


async def test_m25_iteration_rejected_for_legacy_game():
    api = make_api("m24", httpx.MockTransport(lambda r: httpx.Response(200)))
    with pytest.raises(ValueError, match="Invalid iteration"):
        await api.get_players("1-base")


async def test_client_error_raises():
    transport = httpx.MockTransport(lambda r: httpx.Response(404))
    api = make_api("m24", transport)
    with pytest.raises(MaddenAPIError) as excinfo:
        await api.get_players()
    assert excinfo.value.status_code == 404


async def test_server_error_retries_then_succeeds():
    players = [make_legacy_player(1)]
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(request)
        if len(attempts) < 3:
            return httpx.Response(503)
        return httpx.Response(200, json={"count": 1, "docs": players})

    api = make_api("m24", httpx.MockTransport(handler), max_retries=3)
    api._backoff_base = 0

    result = await api.get_players()
    assert len(result) == 1
    assert len(attempts) == 3


async def test_network_error_exhausts_retries():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    api = make_api("m24", httpx.MockTransport(handler), max_retries=0)
    with pytest.raises(MaddenConnectionError):
        await api.get_players()


async def test_cache_hit_avoids_second_fetch():
    players = [make_legacy_player(1)]
    transport, calls = legacy_transport(players)
    api = make_api("m24", transport, cache_ttl=300)

    first = await api.get_players()
    second = await api.get_players()

    assert first == second
    assert len(calls) == 1

    api.clear_cache()
    await api.get_players()
    assert len(calls) == 2


async def test_context_manager_reuses_client():
    players = [make_legacy_player(1)]
    transport, _ = legacy_transport(players)
    async with make_api("m24", transport) as api:
        result = await api.get_players()
        assert len(result) == 1
    assert api._client is None  # closed on exit


async def test_get_player_count():
    players = [make_legacy_player(i) for i in range(1, 43)]
    transport, calls = legacy_transport(players)
    api = make_api("m24", transport)

    assert await api.get_player_count() == 42
    assert len(calls) == 1


def test_get_players_sync():
    players = [make_legacy_player(1)]
    transport, _ = legacy_transport(players)
    api = make_api("m24", transport)

    result = api.get_players_sync()
    assert len(result) == 1
    assert isinstance(result[0], PlayerRating)


async def test_game_version_enum_accepted():
    players = [make_legacy_player(1)]
    transport, _ = legacy_transport(players)
    api = make_api(GameVersion.M22, transport)
    result = await api.get_players()
    assert len(result) == 1


async def test_non_json_response_raises_validation_error():
    from pymadden.exceptions import MaddenValidationError

    transport = httpx.MockTransport(lambda r: httpx.Response(200, content=b"not json"))
    api = make_api("m24", transport)
    with pytest.raises(MaddenValidationError):
        await api.get_players()


async def test_unexpected_shape_raises_validation_error():
    from pymadden.exceptions import MaddenValidationError

    transport = httpx.MockTransport(
        lambda r: httpx.Response(200, content=json.dumps({"weird": True}))
    )
    api = make_api("m24", transport)
    with pytest.raises(MaddenValidationError):
        await api.get_players()
