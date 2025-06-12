import pytest
from pymadden import MaddenAPI
from pymadden.config import Config


def test_invalid_game_years():
    """Test various invalid game year inputs"""
    invalid_years = [
        "m21",  # Too old
        "m25",  # Future year
        "M24",  # Wrong case
        "2024", # Wrong format
        "",     # Empty string
        None,   # None
        123,    # Integer
        "invalid"  # Random string
    ]
    
    for invalid_year in invalid_years:
        with pytest.raises(ValueError, match="Invalid game_year"):
            MaddenAPI(invalid_year)


@pytest.mark.asyncio
async def test_invalid_iterations():
    """Test various invalid iteration inputs"""
    api = MaddenAPI("m24")
    
    invalid_iterations = [
        "week-19",      # Too high
        "week-0",       # Too low  
        "WEEK-1",       # Wrong case
        "week_1",       # Wrong format
        "",             # Empty string
        None,           # None
        123,            # Integer
        "invalid-week"  # Random string
    ]
    
    for invalid_iteration in invalid_iterations:
        with pytest.raises(ValueError, match="Invalid iteration"):
            await api.get_players(invalid_iteration)


def test_config_constants():
    """Test that configuration constants are properly defined"""
    # Test BASE_URL is valid
    assert Config.BASE_URL.startswith("https://")
    assert "ratings-api.ea.com" in Config.BASE_URL
    
    # Test RATINGS_PATHS has expected game years
    expected_years = ["m22", "m23", "m24"]
    for year in expected_years:
        assert year in Config.RATINGS_PATHS
        assert isinstance(Config.RATINGS_PATHS[year], str)
        assert len(Config.RATINGS_PATHS[year]) > 0
    
    # Test ITERATIONS has expected values
    expected_iterations = [
        "launch-ratings", "week-1", "super-bowl"
    ]
    for iteration in expected_iterations:
        assert iteration in Config.ITERATIONS
    
    # Test all iterations are strings
    assert all(isinstance(iteration, str) for iteration in Config.ITERATIONS)
    assert len(Config.ITERATIONS) > 20  # Should have many iterations


def test_api_initialization_edge_cases():
    """Test MaddenAPI initialization with edge cases"""
    # Test with valid game years
    for game_year in Config.RATINGS_PATHS.keys():
        api = MaddenAPI(game_year)
        assert api.ratings_path == Config.RATINGS_PATHS[game_year]
        assert api.base_url == Config.BASE_URL
    
    # Test default initialization
    api_default = MaddenAPI()  # Should default to m23
    assert api_default.ratings_path == Config.RATINGS_PATHS["m23"]


def test_parameter_types():
    """Test that parameters accept correct types"""
    api = MaddenAPI("m24")
    
    # Valid string iteration should work
    # (We can't easily test async methods here without mocking, 
    # but we can test the parameter validation logic)
    
    # Test that the validation logic exists
    assert "launch-ratings" in Config.ITERATIONS
    assert "week-1" in Config.ITERATIONS


@pytest.mark.asyncio 
async def test_boundary_values():
    """Test boundary values for iterations"""
    api = MaddenAPI("m24")
    
    # Test first and last valid iterations
    first_iteration = "launch-ratings"
    last_iteration = "super-bowl"
    
    assert first_iteration in Config.ITERATIONS
    assert last_iteration in Config.ITERATIONS
    
    # These should not raise validation errors (but may fail on API call)
    try:
        await api.get_players(first_iteration)
    except ValueError as e:
        if "Invalid iteration" in str(e):
            pytest.fail("Valid iteration was rejected")
    except Exception:
        pass  # Other exceptions are OK for this test
    
    try:
        await api.get_players(last_iteration)  
    except ValueError as e:
        if "Invalid iteration" in str(e):
            pytest.fail("Valid iteration was rejected")
    except Exception:
        pass  # Other exceptions are OK for this test


def test_case_sensitivity():
    """Test that parameters are case-sensitive as expected"""
    # Game years should be case-sensitive
    with pytest.raises(ValueError):
        MaddenAPI("M24")  # Should be lowercase
    
    with pytest.raises(ValueError): 
        MaddenAPI("m24".upper())


def test_special_characters_in_params():
    """Test handling of special characters in parameters"""
    invalid_params = [
        "m24;DROP TABLE;",  # SQL injection attempt
        "m24<script>",      # XSS attempt  
        "m24\x00",          # Null byte
        "m24\n\r",          # Newlines
        "m24 ",             # Trailing space
        " m24",             # Leading space
    ]
    
    for invalid_param in invalid_params:
        with pytest.raises(ValueError):
            MaddenAPI(invalid_param) 