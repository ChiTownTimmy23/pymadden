# tests/test_api.py
from unittest.mock import MagicMock, patch
import pytest
from pymadden.api import EARatingsAPI
from pymadden.models import RatingsResponse, PlayerRating

def test_api_initialization():
    api = EARatingsAPI("m23-ratings")
    assert api.game_version == "m23-ratings"