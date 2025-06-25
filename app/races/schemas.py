from datetime import datetime
from typing import List, Optional

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)

from app.constants import RACE_RARITIES, RACE_SIZES


class RaceBase(BaseModel):
    """Base schema for Race"""

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Race name",
        examples=["Люди", "Гориусы", "Кобы"],
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Race description"
    )
    size: str = Field(default="Средний", description="Size of race representatives")
    special_traits: Optional[str] = Field(
        None, max_length=1000, description="Special features of the race"
    )
    is_playable: bool = Field(..., description="Is the race available for players")
    rarity: str = Field(default="обычная", description="Race rarity in the world")

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate and clean race name"""
        if not v or not v.strip():
            raise ValueError("Race name cannot be empty")
        return v.strip()

    @field_validator("size")
    def validate_size(cls, v: str) -> str:
        """Validate race size"""
        if v not in RACE_SIZES:
            raise ValueError(f'Size should be one of: {", ".join(RACE_SIZES)}')
        return v

    @field_validator("rarity")
    def validate_rarity(cls, v: str) -> str:
        """Validate race rarity"""
        if v not in RACE_RARITIES:
            raise ValueError(f'Rarity should be one of: {", ".join(RACE_RARITIES)}')
        return v

    @field_validator("description")
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean description"""
        if v is None:
            return v
        if len(v.strip()) == 0:
            return None
        if len(v) > 2000:
            raise ValueError("Description should not exceed 2000 characters")
        return v.strip()

    @field_validator("special_traits")
    def validate_special_traits(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean special traits"""
        if v is None:
            return v
        if len(v.strip()) == 0:
            return None
        if len(v) > 1000:
            raise ValueError("Special traits should not exceed 1000 characters")
        return v.strip()


class RaceCreate(RaceBase):
    """Schema for creating a new race"""

    pass


class RaceUpdate(RaceBase):
    """Schema for updating a race"""

    name: Optional[str] = Field(  # type: ignore
        None, min_length=2, max_length=100, description="New race name"
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="New race description"
    )
    size: Optional[str] = Field(None, description="New race size")  # type: ignore
    special_traits: Optional[str] = Field(
        None, max_length=1000, description="New special traits"
    )
    is_playable: Optional[bool] = Field(None, description="Change playable status")  # type: ignore
    rarity: Optional[str] = Field(None, description="New race rarity")  # type: ignore

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        """Check that at least one field is provided for update"""
        field_values = [
            self.name,
            self.description,
            self.size,
            self.special_traits,
            self.is_playable,
            self.rarity,
        ]
        if all(value is None for value in field_values):
            raise ValueError("At least one field should be provided for update")
        return self


class RaceResponse(RaceBase):
    """Schema for race response"""

    id: int = Field(..., description="Unique race identifier")
    created_at: datetime = Field(..., description="Record creation date")
    updated_at: datetime = Field(..., description="Last update date")

    model_config = ConfigDict(from_attributes=True)


class RaceListResponse(BaseModel):
    """Schema for race list with pagination metadata"""

    races: List[RaceResponse] = Field(..., description="List of races")
    total: int = Field(..., description="Total number of races")
    page: int = Field(..., description="Page number")
    size: int = Field(..., description="Page size")
