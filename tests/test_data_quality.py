import pytest
from unittest.mock import AsyncMock, patch
from pymadden import MaddenAPI, PlayerRating


@pytest.mark.asyncio
async def test_player_rating_ranges():
    """Test that player ratings are within expected ranges"""
    with patch("aiohttp.ClientSession.get") as mock_get:
        # Create mock data with various rating values
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 3,
            "docs": [
                create_mock_player("TestPlayer1", overall_rating=99, speed_rating=95),
                create_mock_player("TestPlayer2", overall_rating=50, speed_rating=60),
                create_mock_player("TestPlayer3", overall_rating=1, speed_rating=10),
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        api = MaddenAPI("m24")
        players = await api.get_players("launch-ratings")
        
        for player in players:
            # Test overall rating range
            assert 1 <= player.overall_rating <= 99, f"Invalid overall rating: {player.overall_rating}"
            
            # Test individual skill ratings
            assert 1 <= player.speed_rating <= 99, f"Invalid speed rating: {player.speed_rating}"
            assert 1 <= player.awareness_rating <= 99, f"Invalid awareness rating: {player.awareness_rating}"
            assert 1 <= player.strength_rating <= 99, f"Invalid strength rating: {player.strength_rating}"


@pytest.mark.asyncio
async def test_player_physical_attributes():
    """Test that player physical attributes are realistic"""
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 2,
            "docs": [
                create_mock_player("Tall Player", height=84, weight=350),  # Very tall/heavy
                create_mock_player("Short Player", height=66, weight=150), # Short/light
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        api = MaddenAPI("m24")
        players = await api.get_players("launch-ratings")
        
        for player in players:
            # Height should be realistic (in inches, roughly 5'6" - 7'0")
            assert 60 <= player.height <= 90, f"Unrealistic height: {player.height}"
            
            # Weight should be realistic (pounds, roughly 150-400 lbs)
            assert 100 <= player.weight <= 450, f"Unrealistic weight: {player.weight}"
            
            # Age should be realistic (18-45 years old)
            assert 18 <= player.age <= 45, f"Unrealistic age: {player.age}"


@pytest.mark.asyncio
async def test_position_specific_attributes():
    """Test that certain positions have appropriate attribute patterns"""
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 3,
            "docs": [
                create_mock_player("QB Player", position="QB", throwPower_rating=90, speed_rating=70),
                create_mock_player("RB Player", position="RB", speed_rating=90, carrying_rating=85),
                create_mock_player("OL Player", position="C", strength_rating=90, speed_rating=40),
            ]
        }
        mock_get.return_value.__aender__.return_value = mock_response
        
        api = MaddenAPI("m24")
        players = await api.get_players("launch-ratings")
        
        for player in players:
            if player.position == "QB":
                # QBs should have decent throwing attributes
                assert player.throwPower_rating >= 60, "QB should have decent throw power"
                assert player.throwAccuracyShort_rating >= 60, "QB should have decent short accuracy"
            
            elif player.position == "RB":
                # RBs should have good speed and carrying
                assert player.speed_rating >= 70, "RB should have decent speed"
                assert player.carrying_rating >= 70, "RB should have decent carrying"
            
            elif player.position in ["LT", "LG", "C", "RG", "RT"]:
                # Offensive linemen should have good strength
                assert player.strength_rating >= 70, "OL should have good strength"


@pytest.mark.asyncio 
async def test_data_consistency():
    """Test internal data consistency"""
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 2,
            "docs": [
                create_mock_player("Player One", firstName="John", lastName="Doe", 
                                 fullNameForSearch="John Doe"),
                create_mock_player("Player Two", firstName="Jane", lastName="Smith",
                                 fullNameForSearch="Jane Smith"),
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        api = MaddenAPI("m24")
        players = await api.get_players("launch-ratings")
        
        for player in players:
            # Full name should match first + last name
            expected_full_name = f"{player.firstName} {player.lastName}"
            assert player.fullNameForSearch == expected_full_name, \
                f"Name mismatch: {player.fullNameForSearch} vs {expected_full_name}"
            
            # Jersey numbers should be valid (0-99)
            assert 0 <= player.jerseyNum <= 99, f"Invalid jersey number: {player.jerseyNum}"
            
            # Years pro should be reasonable (0-20)
            assert 0 <= player.yearsPro <= 25, f"Invalid years pro: {player.yearsPro}"


@pytest.mark.asyncio
async def test_required_fields_not_empty():
    """Test that required string fields are not empty"""
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "count": 1,
            "docs": [create_mock_player("Test Player")]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        api = MaddenAPI("m24")
        players = await api.get_players("launch-ratings")
        
        player = players[0]
        
        # Required string fields should not be empty
        assert len(player.firstName.strip()) > 0, "First name cannot be empty"
        assert len(player.lastName.strip()) > 0, "Last name cannot be empty"
        assert len(player.position.strip()) > 0, "Position cannot be empty"
        assert len(player.team.strip()) > 0, "Team cannot be empty"
        assert len(player.college.strip()) > 0, "College cannot be empty"


def create_mock_player(name, **overrides):
    """Helper function to create mock player data"""
    base_data = {
        "college": "Test University",
        "awareness_rating": 85,
        "throwPower_rating": 80,
        "kickReturn_rating": 70,
        "leadBlock_rating": 65,
        "strength_rating": 80,
        "bCVision_rating": 75,
        "catchInTraffic_rating": 80,
        "playAction_rating": 75,
        "pursuit_rating": 75,
        "plyrAssetname": name,
        "mediumRouteRunning_rating": 75,
        "catching_rating": 80,
        "acceleration_rating": 85,
        "spinMove_rating": 75,
        "height": 72,
        "finesseMoves_rating": 75,
        "spectacularCatch_rating": 80,
        "runBlock_rating": 70,
        "tackle_rating": 70,
        "injury_rating": 85,
        "zoneCoverage_rating": 75,
        "weight": 200,
        "plyrBirthdate": "1/1/1995",
        "runningStyle_rating": "Default",
        "deepRouteRunning_rating": 70,
        "firstName": name.split()[0],
        "lastName": name.split()[-1] if len(name.split()) > 1 else "Player",
        "yearsPro": 3,
        "totalSalary": 2000000,
        "trucking_rating": 75,
        "throwAccuracyShort_rating": 80,
        "position": "WR",
        "jukeMove_rating": 80,
        "playRecognition_rating": 80,
        "shortRouteRunning_rating": 85,
        "status": "published",
        "jerseyNum": 10,
        "breakSack_rating": 75,
        "speed_rating": 85,
        "runBlockPower_rating": 70,
        "jumping_rating": 80,
        "toughness_rating": 85,
        "throwOnTheRun_rating": 75,
        "manCoverage_rating": 70,
        "stiffArm_rating": 75,
        "powerMoves_rating": 70,
        "iteration": "launch-ratings",
        "release_rating": 80,
        "hitPower_rating": 75,
        "throwAccuracyMid_rating": 75,
        "kickAccuracy_rating": 60,
        "passBlockPower_rating": 65,
        "impactBlocking_rating": 70,
        "stamina_rating": 85,
        "carrying_rating": 80,
        "breakTackle_rating": 80,
        "plyrPortrait": 1,
        "kickPower_rating": 65,
        "plyrHandedness": "Right",
        "throwUnderPressure_rating": 75,
        "team": "Test Team",
        "signingBonus": 500000,
        "passBlock_rating": 65,
        "changeOfDirection_rating": 80,
        "press_rating": 70,
        "throwAccuracyDeep_rating": 70,
        "archetype": "WR_Possession",
        "blockShedding_rating": 65,
        "runBlockFinesse_rating": 65,
        "teamId": 1,
        "agility_rating": 80,
        "fullNameForSearch": name,
        "overall_rating": 85,
        "passBlockFinesse_rating": 60,
        "age": 25,
        "primaryKey": 1,
    }
    
    # Apply any overrides
    base_data.update(overrides)
    return base_data 