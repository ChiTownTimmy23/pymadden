# test_api.py
import pytest

from pymadden.api import EARatingsAPI
from pymadden.models import PlayerRating


def test_valid_game_version():
    # Arrange
    game_version = "m22-ratings"

    # Act
    api = EARatingsAPI(game_version)

    # Assert
    assert api.game_version == game_version


def test_invalid_game_version():
    # Arrange
    game_version = "invalid-version"

    # Act & Assert
    with pytest.raises(ValueError):
        EARatingsAPI(game_version)


def test_valid_week_number():
    # Arrange
    week_number = 5
    api = EARatingsAPI("m22-ratings")

    # Act
    api._validate_week_number(week_number)

    # Assert
    # No exception should be raised


def test_invalid_week_number():
    # Arrange
    week_number = -1
    api = EARatingsAPI("m22-ratings")

    # Act & Assert
    with pytest.raises(ValueError):
        api._validate_week_number(week_number)


def test_get_ratings():
    # Arrange
    api = EARatingsAPI("m22-ratings")

    # Act
    ratings = api.get_ratings()

    # Assert
    assert isinstance(ratings, list)
    assert all(isinstance(rating, PlayerRating) for rating in ratings)


def test_get_ratings_by_week():
    # Arrange
    api = EARatingsAPI("m22-ratings")
    week_number = 5

    # Act
    ratings = api.get_ratings_by_week(week_number)

    # Assert
    assert isinstance(ratings, list)
    assert all(isinstance(rating, PlayerRating) for rating in ratings)


def test_get_ratings_by_invalid_week():
    # Arrange
    api = EARatingsAPI("m22-ratings")
    week_number = -1

    # Act & Assert
    with pytest.raises(ValueError):
        api.get_ratings_by_week(week_number)
