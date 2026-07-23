"""Pydantic models for the EA Madden ratings APIs.

Two response shapes are supported:

- Legacy API (Madden 22-24): flat documents with ``*_rating`` fields.
- Drop API (Madden 25): nested structs (position/team/archetype/stats) that can
  be unpacked into a flat record via :meth:`M25Player.to_flat_dict`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PlayerRating(BaseModel):
    """A single player's ratings from the legacy API (Madden 22-24)."""

    model_config = ConfigDict(extra="allow")

    # Identity / bio
    primaryKey: int
    firstName: str
    lastName: str
    fullNameForSearch: str
    position: str
    team: str
    teamId: int
    jerseyNum: int
    age: int
    height: int
    weight: int
    college: str
    yearsPro: int
    archetype: str
    iteration: str
    status: str
    plyrAssetname: str
    plyrBirthdate: str
    plyrHandedness: str
    plyrPortrait: int
    totalSalary: int
    signingBonus: int
    runningStyle_rating: str

    # Ratings
    overall_rating: int
    acceleration_rating: int
    agility_rating: int
    awareness_rating: int
    bCVision_rating: int
    blockShedding_rating: int
    breakSack_rating: int
    breakTackle_rating: int
    carrying_rating: int
    catchInTraffic_rating: int
    catching_rating: int
    changeOfDirection_rating: int
    deepRouteRunning_rating: int
    finesseMoves_rating: int
    hitPower_rating: int
    impactBlocking_rating: int
    injury_rating: int
    jukeMove_rating: int
    jumping_rating: int
    kickAccuracy_rating: int
    kickPower_rating: int
    kickReturn_rating: int
    leadBlock_rating: int
    manCoverage_rating: int
    mediumRouteRunning_rating: int
    passBlockFinesse_rating: int
    passBlockPower_rating: int
    passBlock_rating: int
    playAction_rating: int
    playRecognition_rating: int
    powerMoves_rating: int
    press_rating: int
    pursuit_rating: int
    release_rating: int
    runBlockFinesse_rating: int
    runBlockPower_rating: int
    runBlock_rating: int
    shortRouteRunning_rating: int
    spectacularCatch_rating: int
    speed_rating: int
    spinMove_rating: int
    stamina_rating: int
    stiffArm_rating: int
    strength_rating: int
    tackle_rating: int
    throwAccuracyDeep_rating: int
    throwAccuracyMid_rating: int
    throwAccuracyShort_rating: int
    throwOnTheRun_rating: int
    throwPower_rating: int
    throwUnderPressure_rating: int
    toughness_rating: int
    trucking_rating: int
    zoneCoverage_rating: int

    @property
    def full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def ratings(self) -> dict[str, int]:
        """All numeric ``*_rating`` fields as a ``{stat_name: value}`` dict."""
        return {
            name[: -len("_rating")]: value
            for name, value in self.model_dump().items()
            if name.endswith("_rating") and isinstance(value, int)
        }

    def __str__(self) -> str:
        return (
            f"{self.full_name} ({self.position}, {self.team}) OVR {self.overall_rating}"
        )


class RatingsResponse(BaseModel):
    """Legacy API response wrapper."""

    count: int
    docs: list[PlayerRating]


class LabeledValue(BaseModel):
    """A generic ``{id, label}`` struct used throughout the drop API."""

    model_config = ConfigDict(extra="allow")

    id: Any
    label: str | None = None


class M25Stat(BaseModel):
    """A single stat value with its change since the previous iteration."""

    value: Any
    diff: float = 0


class M25Ability(BaseModel):
    """A player ability (superstar / X-Factor) from the drop API."""

    model_config = ConfigDict(extra="allow")

    id: str
    label: str | None = None
    description: str | None = None
    imageUrl: str | None = None
    type: LabeledValue | None = None


class M25Player(BaseModel):
    """A single player's ratings from the drop API (Madden 25)."""

    model_config = ConfigDict(extra="allow")

    id: int
    firstName: str
    lastName: str
    birthdate: str | None = None
    college: str | None = None
    height: int | None = None
    weight: int | None = None
    age: int | None = None
    jerseyNum: int | None = None
    yearsPro: int | None = None
    handedness: int | None = None
    avatarUrl: str | None = None
    overallRating: int
    position: LabeledValue | None = None
    team: LabeledValue | None = None
    archetype: LabeledValue | None = None
    iteration: LabeledValue | None = None
    stats: dict[str, M25Stat] = Field(default_factory=dict)
    playerAbilities: list[M25Ability] = Field(default_factory=list)

    @property
    def full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"

    @property
    def position_id(self) -> str | None:
        return str(self.position.id) if self.position else None

    @property
    def team_name(self) -> str | None:
        return self.team.label if self.team else None

    def stat(self, name: str) -> Any | None:
        """Look up a stat value by name, e.g. ``player.stat("speed")``."""
        entry = self.stats.get(name)
        return entry.value if entry else None

    def to_flat_dict(self) -> dict[str, Any]:
        """Unpack nested structs into a flat record.

        Stats become ``{stat}_rating`` keys (matching the legacy API naming),
        struct fields collapse to their ids/labels, and abilities become a
        list of labels. Useful for CSV export or DataFrame construction.
        """
        flat: dict[str, Any] = {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "fullName": self.full_name,
            "birthdate": self.birthdate,
            "college": self.college,
            "height": self.height,
            "weight": self.weight,
            "age": self.age,
            "jerseyNum": self.jerseyNum,
            "yearsPro": self.yearsPro,
            "handedness": self.handedness,
            "avatarUrl": self.avatarUrl,
            "overall_rating": self.overallRating,
            "position": self.position_id,
            "positionLabel": self.position.label if self.position else None,
            "team": self.team_name,
            "teamId": self.team.id if self.team else None,
            "archetype": str(self.archetype.id) if self.archetype else None,
            "iteration": str(self.iteration.id) if self.iteration else None,
            "abilities": [a.label or a.id for a in self.playerAbilities],
        }
        for name, entry in self.stats.items():
            flat[f"{name}_rating"] = entry.value
            if entry.diff:
                flat[f"{name}_diff"] = entry.diff
        # overallRating is canonical; don't let the stats block shadow it.
        flat["overall_rating"] = self.overallRating
        return flat

    def __str__(self) -> str:
        pos = self.position_id or "?"
        team = self.team_name or "?"
        return f"{self.full_name} ({pos}, {team}) OVR {self.overallRating}"


class M25RatingsResponse(BaseModel):
    """Drop API response wrapper."""

    model_config = ConfigDict(extra="allow")

    items: list[M25Player]
    totalItems: int
