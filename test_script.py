# test_script.py
import asyncio
import time
from pprint import pprint
from pymadden import MaddenAPI
from pymadden.config import Config

async def test_basic_functionality():
    """Test basic API functionality"""
    print("=" * 50)
    print("TESTING BASIC FUNCTIONALITY")
    print("=" * 50)
    
    api = MaddenAPI("m24")
    
    try:
        # Get some ratings data
        ratings = await api.get_players()
        print(f"✓ Retrieved {len(ratings)} players")
        
        # Print first 5 players as examples
        if ratings:
            print("\nFirst 5 players:")
            for i, player in enumerate(ratings[:5], 1):
                print(f"\n{i}. {player.firstName} {player.lastName} ({player.position}) - {player.team}")
                print(f"   Overall: {player.overall_rating}, Speed: {player.speed_rating}")
                
    except Exception as e:
        print(f"✗ Error: {e}")

async def test_different_game_years():
    """Test different game years"""
    print("\n" + "=" * 50)
    print("TESTING DIFFERENT GAME YEARS")
    print("=" * 50)
    
    for game_year in Config.RATINGS_PATHS.keys():
        try:
            api = MaddenAPI(game_year)
            players = await api.get_players("launch-ratings")
            print(f"✓ {game_year}: {len(players)} players")
        except Exception as e:
            print(f"✗ {game_year}: Error - {e}")

async def test_different_iterations():
    """Test different iterations"""
    print("\n" + "=" * 50)
    print("TESTING DIFFERENT ITERATIONS")
    print("=" * 50)
    
    api = MaddenAPI("m24")
    test_iterations = ["launch-ratings", "week-1", "week-2"]
    
    for iteration in test_iterations:
        try:
            players = await api.get_players(iteration)
            print(f"✓ {iteration}: {len(players)} players")
        except Exception as e:
            print(f"✗ {iteration}: Error - {e}")

async def test_data_quality():
    """Test data quality and consistency"""
    print("\n" + "=" * 50)
    print("TESTING DATA QUALITY")
    print("=" * 50)
    
    api = MaddenAPI("m24")
    
    try:
        players = await api.get_players("launch-ratings")
        print(f"Analyzing {len(players)} players...")
        
        # Check for data quality issues
        issues = []
        
        for player in players[:100]:  # Check first 100 players
            # Check rating ranges
            if not (1 <= player.overall_rating <= 99):
                issues.append(f"Invalid overall rating: {player.overall_rating}")
            
            # Check required fields
            if not player.firstName or not player.lastName:
                issues.append(f"Missing name: {player.firstName} {player.lastName}")
            
            # Check physical attributes
            if not (60 <= player.height <= 90):
                issues.append(f"Unrealistic height: {player.height}")
            
            if not (100 <= player.weight <= 450):
                issues.append(f"Unrealistic weight: {player.weight}")
        
        if issues:
            print(f"✗ Found {len(issues)} data quality issues:")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"   - {issue}")
        else:
            print("✓ No data quality issues found")
            
    except Exception as e:
        print(f"✗ Error during data quality check: {e}")

async def test_performance():
    """Test API performance"""
    print("\n" + "=" * 50)
    print("TESTING PERFORMANCE")
    print("=" * 50)
    
    api = MaddenAPI("m24")
    
    try:
        # Test response time
        start_time = time.time()
        players = await api.get_players("launch-ratings")
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"✓ Response time: {response_time:.2f} seconds")
        print(f"✓ Players retrieved: {len(players)}")
        
        if response_time < 10:
            print("✓ Performance: Good (< 10 seconds)")
        elif response_time < 20:
            print("⚠ Performance: Acceptable (10-20 seconds)")
        else:
            print("✗ Performance: Slow (> 20 seconds)")
            
    except Exception as e:
        print(f"✗ Performance test error: {e}")

async def test_error_handling():
    """Test error handling"""
    print("\n" + "=" * 50)
    print("TESTING ERROR HANDLING")
    print("=" * 50)
    
    # Test invalid game year
    try:
        MaddenAPI("invalid_year")
        print("✗ Invalid game year should raise error")
    except ValueError:
        print("✓ Invalid game year properly rejected")
    
    # Test invalid iteration
    try:
        api = MaddenAPI("m24")
        await api.get_players("invalid_iteration")
        print("✗ Invalid iteration should raise error")
    except ValueError:
        print("✓ Invalid iteration properly rejected")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

async def main():
    """Run all tests"""
    print("PYMADDEN COMPREHENSIVE TEST SCRIPT")
    print("=" * 50)
    
    await test_basic_functionality()
    await test_different_game_years()
    await test_different_iterations()
    await test_data_quality()
    await test_performance()
    await test_error_handling()
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())