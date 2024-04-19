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
        "week-2",
        "week-3",
        "week-4",
        "week-5",
        "week-6",
        "week-7",
        "week-8",
        "week-9",
        "week-10",
        "week-11",
        "week-12",
        "week-13",
        "week-14",
        "week-15",
        "week-16",
        "week-17",
        "week-18",
        "wild-card-round",
        "divisional-round",
        "conference-championship-round",
        "pro-bowl",
        "super-bowl",
    ]
