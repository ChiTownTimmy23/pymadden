# pymadden
- [] Ideally, I want to create  a PyPI package that returns data for Madden 22, Madden 23, Madden 24, and Madden 25
- [] Need to add proper logging
- [] Would like to use httpx and Pydantic.
- [] Need to organize the project structure to align with best practices of a package
- [] The endpoints for Madden 22, Madden 23, Madden 24 are the same with Madden 25 being a different endpoint

```python

# Madden 22, Madden 23, Madden 24
BASE_URL = "https://ratings-api.ea.com/v2/entities"

# Madden 25
M25_BASE_URL = "https://drop-api.ea.com/rating/madden-nfl"

```

- [] The endpoints have different structures and query parameters.  For example, for Madden 23 it'll be https://ratings-api.ea.com/v2/entities/m23-ratings?filter=iteration:launch-ratings (where the query parameter for 'iteration' can be any one of the Iteration class below).  Similarly, the Madden 25 will be:  https://drop-api.ea.com/rating/madden-nfl/?iteration=1-base&locale=en&limit=100&offset=100 (with the iteration coming from the M25Iteration class).

- [] Would like to use enums where possible
```python

class GameVersion(Enum):
    M22 = "m22"
    M23 = "m23"
    M24 = "m24"
    M25 = "m25"

class Iteration(Enum):
    LAUNCH_RATINGS = "launch-ratings"
    WEEK_1 = "week-1"
    WEEK_2 = "week-2"
    WEEK_3 = "week-3"
    WEEK_4 = "week-4"
    WEEK_5 = "week-5"
    WEEK_6 = "week-6"
    WEEK_7 = "week-7"
    WEEK_8 = "week-8"
    WEEK_9 = "week-9"
    WEEK_10 = "week-10"
    WEEK_11 = "week-11"
    WEEK_12 = "week-12"
    WEEK_13 = "week-13"
    WEEK_14 = "week-14"
    WEEK_15 = "week-15"
    WEEK_16 = "week-16"
    WEEK_17 = "week-17"
    WEEK_18 = "week-18"
    WILD_CARD_ROUND = "wild-card-round"
    DIVISIONAL_ROUND = "divisional-round"
    CONFERENCE_CHAMPIONSHIP_ROUND = "conference-championship-round"
    PRO_BOWL = "pro-bowl"
    SUPER_BOWL = "super-bowl"

class M25Iteration(Enum):
    BASE = "1-base"
```        

- [] The responses from the endpoints are different, so I'd like to be able to account for this in the package somehow.
- [] Would like to add caching, a rate limiter, and any other optimized processes
- [] Want a function that adds on additional features that are derived from columns in the data sets.
- [] Need to unpack the structs in the Madden 25 response.