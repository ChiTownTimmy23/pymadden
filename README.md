# pymadden

Pymadden is a Python library that provides a convenient way to interact with the Electronic Arts (EA) Madden NFL ratings API. It allows you to easily retrieve player ratings data for Madden NFL games.

## Features

- Retrieve player ratings data for Madden NFL games (e.g., Madden 21, Madden 22, Madden 23)
- Filter ratings data by iteration (e.g., launch-ratings, week-1, week-2, etc.)
- Retrieve ratings data for a specific week
- Provides Pydantic models for type validation and easy data manipulation
- Includes unit tests to ensure reliability and maintainability

## Installation

You can install pymadden using Poetry. First, make sure you have [Poetry](https://python-poetry.org/) installed. Then, run the following command:

```bash
poetry add pymadden
```

## Quick Start

Here's a basic example of how to use pymadden to retrieve player ratings data:

```python
from pymadden import EARatingsAPI

# Create an instance of the EARatingsAPI
api = EARatingsAPI("m23-ratings", "sqlite:///ratings.db")

# Retrieve player ratings for the launch iteration
launch_ratings = api.get_ratings()

# Retrieve player ratings for a specific week
week_1_ratings = api.get_ratings_by_week(1)

# Write the ratings data to the database
api.write_ratings_to_db(launch_ratings)
```