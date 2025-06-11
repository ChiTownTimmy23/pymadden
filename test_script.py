# test_script.py
import asyncio
from pymadden import MaddenAPI

async def main():
    api = MaddenAPI("m24")
    
    try:
        # Get some ratings data
        ratings = await api.get_players()
        print(f"Retrieved {len(ratings)} players")
        
        # Print first player as example
        if ratings:
            first_player = ratings[0]
            print(f"First player: {first_player}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())