"""Tests for the pymadden CLI."""

import json

import httpx
import pytest

from pymadden import cli
from pymadden.api import MaddenAPI

from .conftest import make_legacy_player, make_m25_player


@pytest.fixture
def patched_api(monkeypatch):
    """Route MaddenAPI construction in the CLI through a MockTransport."""

    state = {"transport": None}

    original_init = MaddenAPI.__init__

    def patched_init(self, game_version="m24", **kwargs):
        kwargs["transport"] = state["transport"]
        kwargs["requests_per_second"] = 0
        original_init(self, game_version, **kwargs)

    monkeypatch.setattr(MaddenAPI, "__init__", patched_init)
    return state


def legacy_handler(players):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"count": len(players), "docs": players})

    return httpx.MockTransport(handler)


def m25_handler(items):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"items": items, "totalItems": len(items)})

    return httpx.MockTransport(handler)


def test_cli_table_output(patched_api, capsys):
    patched_api["transport"] = legacy_handler(
        [
            make_legacy_player(1, overall_rating=95, position="QB"),
            make_legacy_player(2, overall_rating=80, position="WR"),
        ]
    )
    assert cli.main(["m24"]) == 0
    out = capsys.readouterr().out
    assert "Mock Player1" in out
    assert "2 players" in out
    # sorted by overall descending
    assert out.index("Player1") < out.index("Player2")


def test_cli_json_position_filter(patched_api, capsys):
    patched_api["transport"] = legacy_handler(
        [
            make_legacy_player(1, position="QB"),
            make_legacy_player(2, position="WR"),
        ]
    )
    assert cli.main(["m24", "--position", "qb", "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data) == 1
    assert data[0]["position"] == "QB"


def test_cli_m25_top_n(patched_api, capsys):
    patched_api["transport"] = m25_handler(
        [
            make_m25_player(1, overallRating=99),
            make_m25_player(2, overallRating=70),
            make_m25_player(3, overallRating=85),
        ]
    )
    assert cli.main(["m25", "--top", "2", "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [d["overall_rating"] for d in data] == [99, 85]


def test_cli_csv_output(patched_api, capsys):
    patched_api["transport"] = legacy_handler([make_legacy_player(1)])
    assert cli.main(["m24", "--format", "csv"]) == 0
    out = capsys.readouterr().out
    lines = out.strip().splitlines()
    assert len(lines) == 2
    assert "firstName" in lines[0]


def test_cli_team_filter(patched_api, capsys):
    patched_api["transport"] = legacy_handler(
        [
            make_legacy_player(1, team="Chicago Bears"),
            make_legacy_player(2, team="Green Bay Packers"),
        ]
    )
    assert cli.main(["m24", "--team", "bears", "--format", "json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert len(data) == 1
    assert data[0]["team"] == "Chicago Bears"


def test_cli_invalid_iteration_returns_error(patched_api, capsys):
    patched_api["transport"] = legacy_handler([])
    assert cli.main(["m24", "--iteration", "week-99"]) == 2
    assert "Invalid iteration" in capsys.readouterr().err


def test_cli_rejects_unknown_game(capsys):
    with pytest.raises(SystemExit):
        cli.main(["m99"])
