import pytest
import aiohttp
from unittest.mock import AsyncMock, patch
from pymadden import MaddenAPI


@pytest.mark.asyncio
async def test_network_timeout():
    """Test handling of network timeouts"""
    api = MaddenAPI("m24")
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.side_effect = aiohttp.ClientTimeout()
        
        with pytest.raises(aiohttp.ClientTimeout):
            await api.get_players("launch-ratings")


@pytest.mark.asyncio
async def test_http_error_responses():
    """Test handling of HTTP error responses (404, 500, etc.)"""
    api = MaddenAPI("m24")
    
    # Test 404 Not Found
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.json.side_effect = aiohttp.ClientResponseError(
            request_info=None, history=None, status=404
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(aiohttp.ClientResponseError):
            await api.get_players("launch-ratings")


@pytest.mark.asyncio
async def test_malformed_json_response():
    """Test handling of malformed JSON responses"""
    api = MaddenAPI("m24")
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(ValueError):
            await api.get_players("launch-ratings")


@pytest.mark.asyncio
async def test_empty_response():
    """Test handling of empty API responses"""
    api = MaddenAPI("m24")
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"count": 0, "docs": []}
        mock_get.return_value.__aenter__.return_value = mock_response
        
        players = await api.get_players("launch-ratings")
        assert players == []


@pytest.mark.asyncio
async def test_missing_required_fields():
    """Test handling of API responses with missing required fields"""
    api = MaddenAPI("m24")
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        # Response missing required fields
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 1,
            "docs": [
                {
                    "firstName": "Test",
                    # Missing lastName, position, etc.
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception):  # Should raise validation error
            await api.get_players("launch-ratings")


@pytest.mark.asyncio
async def test_invalid_data_types():
    """Test handling of invalid data types in API response"""
    api = MaddenAPI("m24")
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 1,
            "docs": [
                {
                    "firstName": "Test",
                    "lastName": "Player",
                    "position": "QB",
                    "overall_rating": "not_a_number",  # Should be int
                    "age": "twenty-five",  # Should be int
                    # ... include other required fields with correct types
                    "college": "Test University",
                    "awareness_rating": 85,
                    "throwPower_rating": 90,
                    "kickReturn_rating": 75,
                    "leadBlock_rating": 65,
                    "strength_rating": 85,
                    "bCVision_rating": 80,
                    "catchInTraffic_rating": 80,
                    "playAction_rating": 75,
                    "pursuit_rating": 80,
                    "plyrAssetname": "TestPlayer",
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
                    "plyrBirthdate": "1/1/1990",
                    "runningStyle_rating": "Default",
                    "deepRouteRunning_rating": 70,
                    "yearsPro": 3,
                    "totalSalary": 3000000,
                    "trucking_rating": 75,
                    "throwAccuracyShort_rating": 80,
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
                    "team": "Test Team",
                    "signingBonus": 500000,
                    "passBlock_rating": 70,
                    "changeOfDirection_rating": 80,
                    "press_rating": 70,
                    "throwAccuracyDeep_rating": 70,
                    "archetype": "QB_Scrambler",
                    "blockShedding_rating": 65,
                    "runBlockFinesse_rating": 70,
                    "teamId": 1,
                    "agility_rating": 85,
                    "fullNameForSearch": "Test Player",
                    "passBlockFinesse_rating": 65,
                    "primaryKey": 1,
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        with pytest.raises(Exception):  # Should raise validation error
            await api.get_players("launch-ratings") 