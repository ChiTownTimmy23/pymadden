import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pymadden.api import MaddenAPI
from pymadden.config import Config
from pymadden.models import PlayerRating


@pytest.mark.asyncio
async def test_get_players():
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 2,
            "docs": [
                {
                    "college": "Mock University 1",
                    "awareness_rating": 85,
                    "throwPower_rating": 90,
                    "kickReturn_rating": 75,
                    "leadBlock_rating": 65,
                    "strength_rating": 85,
                    "bCVision_rating": 80,
                    "catchInTraffic_rating": 80,
                    "playAction_rating": 75,
                    "pursuit_rating": 80,
                    "plyrAssetname": "MockPlayer1",
                    "mediumRouteRunning_rating": 75,
                    "catching_rating": 80,
                    "acceleration_rating": 85,
                    "spinMove_rating": 80,
                    "height": 70,
                    "finesseMoves_rating": 75,
                    "spectacularCatch_rating": 80,
                    "runBlock_rating": 75,
                    "tackle_rating": 70,
                    "injury_rating": 85,
                    "zoneCoverage_rating": 75,
                    "weight": 190,
                    "plyrBirthdate": "2/2/1992",
                    "runningStyle_rating": "Default Stride Tight",
                    "deepRouteRunning_rating": 70,
                    "firstName": "Mock",
                    "lastName": "Player1",
                    "yearsPro": 3,
                    "totalSalary": 3000000,
                    "trucking_rating": 75,
                    "throwAccuracyShort_rating": 80,
                    "position": "WR",
                    "jukeMove_rating": 85,
                    "playRecognition_rating": 80,
                    "shortRouteRunning_rating": 85,
                    "status": "published",
                    "jerseyNum": 20,
                    "breakSack_rating": 75,
                    "speed_rating": 85,
                    "runBlockPower_rating": 75,
                    "jumping_rating": 80,
                    "toughness_rating": 85,
                    "throwOnTheRun_rating": 75,
                    "manCoverage_rating": 70,
                    "stiffArm_rating": 80,
                    "powerMoves_rating": 75,
                    "iteration": "launch-ratings",
                    "release_rating": 80,
                    "hitPower_rating": 75,
                    "throwAccuracyMid_rating": 75,
                    "kickAccuracy_rating": 65,
                    "passBlockPower_rating": 70,
                    "impactBlocking_rating": 75,
                    "stamina_rating": 85,
                    "carrying_rating": 90,
                    "breakTackle_rating": 85,
                    "plyrPortrait": 2,
                    "kickPower_rating": 65,
                    "plyrHandedness": "Right",
                    "throwUnderPressure_rating": 75,
                    "team": "Mock Team 1",
                    "signingBonus": 500000,
                    "passBlock_rating": 70,
                    "changeOfDirection_rating": 80,
                    "press_rating": 70,
                    "throwAccuracyDeep_rating": 70,
                    "archetype": "RB_Elusive",
                    "blockShedding_rating": 65,
                    "runBlockFinesse_rating": 70,
                    "teamId": 1,
                    "agility_rating": 85,
                    "fullNameForSearch": "Mock Player2",
                    "overall_rating": 95,
                    "passBlockFinesse_rating": 65,
                    "age": 26,
                    "primaryKey": 1,
                },
                {
                    "college": "Mock University 2",
                    "awareness_rating": 85,
                    "throwPower_rating": 90,
                    "kickReturn_rating": 75,
                    "leadBlock_rating": 65,
                    "strength_rating": 85,
                    "bCVision_rating": 80,
                    "catchInTraffic_rating": 80,
                    "playAction_rating": 75,
                    "pursuit_rating": 80,
                    "plyrAssetname": "MockPlayer2",
                    "mediumRouteRunning_rating": 75,
                    "catching_rating": 80,
                    "acceleration_rating": 85,
                    "spinMove_rating": 80,
                    "height": 70,
                    "finesseMoves_rating": 75,
                    "spectacularCatch_rating": 80,
                    "runBlock_rating": 75,
                    "tackle_rating": 70,
                    "injury_rating": 85,
                    "zoneCoverage_rating": 75,
                    "weight": 190,
                    "plyrBirthdate": "2/2/1992",
                    "runningStyle_rating": "Default Stride Tight",
                    "deepRouteRunning_rating": 70,
                    "firstName": "Mock",
                    "lastName": "Player2",
                    "yearsPro": 3,
                    "totalSalary": 3000000,
                    "trucking_rating": 75,
                    "throwAccuracyShort_rating": 80,
                    "position": "RB",
                    "jukeMove_rating": 85,
                    "playRecognition_rating": 80,
                    "shortRouteRunning_rating": 85,
                    "status": "published",
                    "jerseyNum": 20,
                    "breakSack_rating": 75,
                    "speed_rating": 85,
                    "runBlockPower_rating": 75,
                    "jumping_rating": 80,
                    "toughness_rating": 85,
                    "throwOnTheRun_rating": 75,
                    "manCoverage_rating": 70,
                    "stiffArm_rating": 80,
                    "powerMoves_rating": 75,
                    "iteration": "launch-ratings",
                    "release_rating": 80,
                    "hitPower_rating": 75,
                    "throwAccuracyMid_rating": 75,
                    "kickAccuracy_rating": 65,
                    "passBlockPower_rating": 70,
                    "impactBlocking_rating": 75,
                    "stamina_rating": 85,
                    "carrying_rating": 90,
                    "breakTackle_rating": 85,
                    "plyrPortrait": 2,
                    "kickPower_rating": 65,
                    "plyrHandedness": "Right",
                    "throwUnderPressure_rating": 75,
                    "team": "Mock Team 2",
                    "signingBonus": 500000,
                    "passBlock_rating": 70,
                    "changeOfDirection_rating": 80,
                    "press_rating": 70,
                    "throwAccuracyDeep_rating": 70,
                    "archetype": "RB_Elusive",
                    "blockShedding_rating": 65,
                    "runBlockFinesse_rating": 70,
                    "teamId": 2,
                    "agility_rating": 85,
                    "fullNameForSearch": "Mock Player2",
                    "overall_rating": 92,
                    "passBlockFinesse_rating": 65,
                    "age": 26,
                    "primaryKey": 2,
                },
            ],
        }
        mock_get.return_value.__aenter__.return_value = mock_response

        api = MaddenAPI()
        player_ratings = await api.get_players()

        assert len(player_ratings) == 2
        assert all(isinstance(rating, PlayerRating) for rating in player_ratings)
        assert player_ratings[0].firstName == "Mock"
        assert player_ratings[0].lastName == "Player1"
        assert player_ratings[0].position == "WR"
        assert player_ratings[0].team == "Mock Team 1"
        assert player_ratings[0].overall_rating == 95
        assert player_ratings[1].firstName == "Mock"
        assert player_ratings[1].lastName == "Player2"
        assert player_ratings[1].position == "RB"
        assert player_ratings[1].team == "Mock Team 2"
        assert player_ratings[1].overall_rating == 92


def test_madden_api_invalid_game_year():
    with pytest.raises(ValueError, match="Invalid game_year"):
        MaddenAPI(game_year="m25")


@pytest.mark.asyncio
async def test_get_players_invalid_iteration():
    api = MaddenAPI()
    with pytest.raises(ValueError, match="Invalid iteration"):
        await api.get_players(iteration="week-20")
