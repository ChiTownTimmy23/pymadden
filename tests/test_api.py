# tests/test_api.py
from unittest.mock import MagicMock, patch
import pytest
from pymadden.client import EARatingsClient
from pymadden.models import RatingsResponse, PlayerRating

def test_api_initialization():
    api = EARatingsClient("m23-ratings")
    assert api.client.game_version == "m23-ratings"