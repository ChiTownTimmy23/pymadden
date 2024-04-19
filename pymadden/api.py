import aiohttp
from typing import List
from .config import Config
from .models import PlayerRating, RatingsResponse


class MaddenAPI:
    def __init__(self, game_year: str = "m23"):
        if game_year not in Config.RATINGS_PATHS:
            raise ValueError(
                f"Invalid game_year. Available options: {', '.join(Config.RATINGS_PATHS.keys())}"
            )
        self.base_url = Config.BASE_URL
        self.ratings_path = Config.RATINGS_PATHS[game_year]

    async def get_players(
        self, iteration: str = "launch-ratings"
    ) -> List[PlayerRating]:
        """
        Retrieve a list of all player ratings for a given iteration.

        :param iteration: The iteration to retrieve player ratings for (e.g., "launch-ratings", "week-1", etc.)
        :return: A list of PlayerRating objects
        :raises ValueError: If the provided iteration is not valid
        """
        if iteration not in Config.ITERATIONS:
            raise ValueError(
                f"Invalid iteration. Available options: {', '.join(Config.ITERATIONS)}"
            )

        url = f"{self.base_url}/{self.ratings_path}?filter=iteration:{iteration}"
        player_ratings = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                total_count = data["count"]
                player_ratings.extend(RatingsResponse(**data).docs)

            page = 1
            while len(player_ratings) < total_count:
                page += 1
                async with session.get(f"{url}&page={page}") as response:
                    data = await response.json()
                    player_ratings.extend(RatingsResponse(**data).docs)

        return player_ratings
