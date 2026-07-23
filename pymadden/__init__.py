"""pymadden: async Python client for the EA Madden NFL ratings APIs."""

from .api import MaddenAPI
from .config import GameVersion, Iteration, M25Iteration
from .exceptions import (
    MaddenAPIError,
    MaddenConnectionError,
    MaddenRateLimitError,
    MaddenValidationError,
    PyMaddenError,
)
from .features import derive_features, derive_features_for_all
from .models import (
    M25Player,
    M25RatingsResponse,
    PlayerRating,
    RatingsResponse,
)

__version__ = "0.2.0"

__all__ = [
    "MaddenAPI",
    "GameVersion",
    "Iteration",
    "M25Iteration",
    "PlayerRating",
    "RatingsResponse",
    "M25Player",
    "M25RatingsResponse",
    "derive_features",
    "derive_features_for_all",
    "PyMaddenError",
    "MaddenAPIError",
    "MaddenConnectionError",
    "MaddenRateLimitError",
    "MaddenValidationError",
    "__version__",
]
