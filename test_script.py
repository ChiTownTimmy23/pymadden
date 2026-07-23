# test_script.py — live smoke test against the real EA APIs.
import asyncio

from pymadden import MaddenAPI, derive_features


async def demo(game: str) -> None:
    print(f"\n=== {game} ===")
    async with MaddenAPI(game) as api:
        players = await api.get_players()
    print(f"Retrieved {len(players)} players")

    top = sorted(
        players,
        key=lambda p: getattr(p, "overall_rating", None)
        or getattr(p, "overallRating", 0),
        reverse=True,
    )[:5]
    for i, player in enumerate(top, 1):
        print(f"  {i}. {player}")

    features = derive_features(top[0])
    print(
        f"  Derived for {features['fullName']}: "
        f"speed_score={features['speed_score']}, bmi={features['bmi']}"
    )


async def main() -> None:
    for game in ("m24", "m25"):
        try:
            await demo(game)
        except Exception as exc:
            print(f"Error for {game}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
