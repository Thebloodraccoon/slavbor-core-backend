from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.constants import RACE_SIZES


class RaceBase(BaseModel):
    """Base schema for Race"""

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Race name",
        examples=["Люди", "Гориусы", "Кобы"],
    )
    description: str | None = Field(None, max_length=2000, description="Race description")
    size: str = Field(default="Средний", description="Size of race representatives")
    is_playable: bool = Field(..., description="Is the race available for players")

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
            raise ValueError(f"Size should be one of: {', '.join(RACE_SIZES)}")
        return v

    @field_validator("description")
    def validate_description(cls, v: str | None) -> str | None:
        """Validate and clean description"""
        if v is None:
            return v
        if len(v.strip()) == 0:
            return None
        if len(v) > 2000:
            raise ValueError("Description should not exceed 2000 characters")
        return v.strip()


class RaceCreate(RaceBase):
    """Schema for creating a new race"""


class RaceUpdate(RaceBase):
    """Schema for updating a race"""

    name: str | None = Field(  # type: ignore
        None, min_length=2, max_length=100, description="New race name"
    )
    description: str | None = Field(None, max_length=2000, description="New race description")
    size: str | None = Field(None, description="New race size")  # type: ignore
    is_playable: bool | None = Field(None, description="Change playable status")  # type: ignore

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        """Check that at least one field is provided for update"""
        field_values = [
            self.name,
            self.description,
            self.size,
            self.is_playable,
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

    races: list[RaceResponse] = Field(..., description="List of races")
    total: int = Field(..., description="Total number of races")
    page: int = Field(..., description="Page number")
    size: int = Field(..., description="Page size")
