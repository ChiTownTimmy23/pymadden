# test_script.py
import asyncio
from pprint import pprint
from pymadden import MaddenAPI

async def main():
    api = MaddenAPI("m24")
    
    try:
        # Get some ratings data
        ratings = await api.get_players()
        print(f"Retrieved {len(ratings)} players")
        
        # Print first 10 players as examples
        if ratings:
            print("\nFirst 10 players:")
            for i, player in enumerate(ratings[:10], 1):
                print(f"\n{i}. Player:")
                pprint(player.dict() if hasattr(player, 'dict') else player.__dict__)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())