"""Command-line interface: ``python -m pymadden`` or the ``pymadden`` script.

Examples::

    pymadden m24 --iteration launch-ratings --top 25
    pymadden m25 --iteration 1-base --position QB --format json
    pymadden m23 --team Bears --format csv > bears.csv
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import io
import json
import logging
import sys
from typing import Any

from .api import MaddenAPI
from .config import GameVersion
from .models import M25Player, PlayerRating


def _flatten(player: Any) -> dict[str, Any]:
    if isinstance(player, M25Player):
        return player.to_flat_dict()
    assert isinstance(player, PlayerRating)
    return player.model_dump()


def _row(flat: dict[str, Any]) -> dict[str, Any]:
    name = flat.get("fullName") or flat.get("fullNameForSearch") or ""
    return {
        "name": name,
        "position": flat.get("position") or "",
        "team": flat.get("team") or "",
        "overall": flat.get("overall_rating") or 0,
        "speed": flat.get("speed_rating") or "",
        "age": flat.get("age") or "",
    }


def _print_table(rows: list[dict[str, Any]]) -> None:
    headers = ["name", "position", "team", "overall", "speed", "age"]
    widths = {
        h: max(len(h), *(len(str(r[h])) for r in rows)) if rows else len(h)
        for h in headers
    }
    line = "  ".join(h.upper().ljust(widths[h]) for h in headers)
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(str(r[h]).ljust(widths[h]) for h in headers))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pymadden",
        description="Fetch EA Madden NFL player ratings.",
    )
    parser.add_argument(
        "game",
        choices=[v.value for v in GameVersion],
        help="Game version (m22, m23, m24, m25)",
    )
    parser.add_argument(
        "-i",
        "--iteration",
        default=None,
        help="Ratings iteration (default: launch ratings)",
    )
    parser.add_argument("-p", "--position", help="Filter by position id (e.g. QB)")
    parser.add_argument("-t", "--team", help="Filter by team name substring")
    parser.add_argument(
        "-n", "--top", type=int, default=0, help="Only show the top N by overall"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Debug logging")
    return parser


async def _run(args: argparse.Namespace) -> int:
    async with MaddenAPI(args.game) as api:
        players = await api.get_players(args.iteration)

    flats = [_flatten(p) for p in players]
    if args.position:
        flats = [
            f
            for f in flats
            if str(f.get("position") or "").upper() == args.position.upper()
        ]
    if args.team:
        needle = args.team.lower()
        flats = [f for f in flats if needle in str(f.get("team") or "").lower()]

    flats.sort(key=lambda f: f.get("overall_rating") or 0, reverse=True)
    if args.top > 0:
        flats = flats[: args.top]

    if args.format == "json":
        print(json.dumps(flats, indent=2, default=str))
    elif args.format == "csv":
        if flats:
            fieldnames = sorted({key for f in flats for key in f})
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flats)
            sys.stdout.write(buffer.getvalue())
    else:
        _print_table([_row(f) for f in flats])
        print(f"\n{len(flats)} players")
    return 0


def main(argv: list[str] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    try:
        return asyncio.run(_run(args))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
