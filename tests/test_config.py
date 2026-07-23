"""Tests for game version parsing and iteration validation."""

import pytest

from pymadden.config import (
    GameVersion,
    Iteration,
    M25Iteration,
    validate_iteration,
)


def test_game_version_parse_strings():
    assert GameVersion.parse("m24") is GameVersion.M24
    assert GameVersion.parse("M25") is GameVersion.M25
    assert GameVersion.parse(GameVersion.M22) is GameVersion.M22


def test_game_version_parse_invalid():
    with pytest.raises(ValueError, match="Invalid game version"):
        GameVersion.parse("madden-2004")


def test_uses_legacy_api():
    assert GameVersion.M22.uses_legacy_api
    assert GameVersion.M24.uses_legacy_api
    assert not GameVersion.M25.uses_legacy_api


def test_validate_iteration_legacy():
    assert validate_iteration(GameVersion.M23, "week-5") == "week-5"
    assert validate_iteration(GameVersion.M23, Iteration.PRO_BOWL) == "pro-bowl"


def test_validate_iteration_m25():
    assert validate_iteration(GameVersion.M25, "9-week-8") == "9-week-8"
    assert validate_iteration(GameVersion.M25, M25Iteration.BASE) == "1-base"


def test_validate_iteration_cross_version_rejected():
    with pytest.raises(ValueError, match="Invalid iteration"):
        validate_iteration(GameVersion.M25, "launch-ratings")
    with pytest.raises(ValueError, match="Invalid iteration"):
        validate_iteration(GameVersion.M22, "1-base")
