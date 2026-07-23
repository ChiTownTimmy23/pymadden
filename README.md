# pymadden

Pymadden is an async Python client for the Electronic Arts (EA) Madden NFL ratings APIs. It retrieves complete player ratings datasets for Madden 22 through Madden 25 behind a single, simple interface.

## Features

- **All four games, one interface** — Madden 22/23/24 (legacy `ratings-api.ea.com`) and Madden 25 (`drop-api.ea.com`), including automatic unpacking of Madden 25's nested response structs
- **Fast** — reusable HTTP connections (httpx) with concurrent page fetching
- **Robust** — retries with exponential backoff, client-side rate limiting, typed exceptions, and TTL response caching
- **Typed** — Pydantic v2 models for every response shape, tolerant of new fields EA adds
- **Derived features** — composite scores (speed, coverage, pass rush, route running, throwing) and BMI computed from raw ratings
- **CLI included** — fetch, filter, sort, and export ratings as a table, JSON, or CSV from your terminal

## Installation

Requires Python 3.10+.

```bash
uv add pymadden        # or: pip install pymadden
```

For development:

```bash
git clone https://github.com/ChiTownTimmy23/pymadden
cd pymadden
uv sync
```

## Quick Start

```python
import asyncio
from pymadden import MaddenAPI, Iteration

async def main():
    async with MaddenAPI("m24") as api:
        players = await api.get_players(Iteration.LAUNCH_RATINGS)

    best = max(players, key=lambda p: p.overall_rating)
    print(f"{best.full_name}: {best.overall_rating} OVR")

asyncio.run(main())
```

### Madden 25

Madden 25 uses a different EA API with nested structs; pymadden parses them into `M25Player` models and can flatten them for you:

```python
import asyncio
from pymadden import MaddenAPI, M25Iteration

async def main():
    async with MaddenAPI("m25") as api:
        players = await api.get_players(M25Iteration.WEEK_8)

    player = players[0]
    print(player.full_name, player.overallRating, player.stat("speed"))
    flat = player.to_flat_dict()   # legacy-style flat dict, e.g. for pandas

asyncio.run(main())
```

### Synchronous usage

```python
from pymadden import MaddenAPI

players = MaddenAPI("m23").get_players_sync("week-1")
```

### Derived features

```python
from pymadden import derive_features

features = derive_features(players[0])
# {'fullName': ..., 'bmi': 27.3, 'speed_score': 94.5, 'coverage_score': ...,
#  'pass_rush_score': ..., 'route_running_score': ..., 'throwing_score': ...,
#  'athleticism_delta': ...}
```

### Client options

```python
api = MaddenAPI(
    "m24",
    timeout=30.0,              # per-request timeout (seconds)
    max_retries=3,             # retries for 5xx/429/network errors
    max_concurrency=4,         # concurrent page requests
    requests_per_second=5.0,   # client-side rate limit (0 disables)
    cache_ttl=300.0,           # response cache TTL in seconds (0 disables)
)
```

### Error handling

```python
from pymadden import MaddenAPI, MaddenAPIError, MaddenConnectionError

try:
    players = await MaddenAPI("m24").get_players()
except MaddenConnectionError:
    ...  # network failure after retries
except MaddenAPIError as exc:
    ...  # HTTP error; exc.status_code available
```

## CLI

```bash
pymadden m24 --top 25                          # top 25 overall, table output
pymadden m25 --position QB --top 10            # best quarterbacks in Madden 25
pymadden m23 --team Bears --format csv > bears.csv
pymadden m24 --iteration week-10 --format json
```

Run `pymadden --help` for all options.

## Development

```bash
just test        # run tests
just test-cov    # tests with coverage
just lint        # ruff check
just format      # ruff format
just check       # all of the above
just smoke       # live end-to-end test against the real EA APIs
```

## Supported iterations

- **Madden 22-24**: `launch-ratings`, `week-1` … `week-18`, `wild-card-round`, `divisional-round`, `conference-championship-round`, `pro-bowl`, `super-bowl`
- **Madden 25**: `1-base`, `2-week-1` … `19-week-18`, `20-wild-card-round`, `21-divisional-round`, `22-conference-championship-round`, `23-super-bowl` (also available via the `M25Iteration` enum)
