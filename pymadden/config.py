from typing import Dict, List


class Config:
    BASE_URL: str = "https://ratings-api.ea.com/v2/entities"
    RATINGS_PATHS: Dict[str, str] = {
        "m22": "m22-ratings",
        "m23": "m23-ratings",
        "m24": "m24-ratings",
    }
    ITERATIONS: List[str] = [
        "launch-ratings",
        "week-1",
        "week-18",
        "wild-card-round",
    ]
