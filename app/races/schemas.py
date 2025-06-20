from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, constr, field_validator, model_validator

from app.races.utils import (validate_race_rarity, validate_race_size,
                             validate_racial_abilities, validate_stat_bonuses,
                             validate_text_field)


class RaceBase(BaseModel):
    name: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(  # type: ignore
        ..., description="Название расы", examples=["Люди", "Гориусы", "Кобы"]
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Описание расы"
    )
    size: str = Field(default="Средний", description="Размер представителей расы")

    @field_validator("size")
    def validate_size_field(cls, v: str) -> str:
        return validate_race_size(v)  # type: ignore

    @field_validator("description")
    def validate_description_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=2000)


class RaceCreate(RaceBase):
    racial_abilities: Optional[List[str]] = Field(
        default=[],
        description="Расовые способности",
        examples=[["Темное зрение", "Магическое сопротивление"]],
    )
    stat_bonuses: Optional[Dict[str, int]] = Field(
        default={},
        description="Бонусы к характеристикам",
        examples=[{"strength": 2, "constitution": 1}],
    )
    languages: Optional[List[str]] = Field(
        default=[],
        description="Известные языки",
        examples=[["Гориуский", "Араратский"]],
    )
    special_traits: Optional[str] = Field(
        None, max_length=1000, description="Особые черты расы"
    )
    average_height: Optional[constr(max_length=50)] = Field(  # type: ignore
        None, description="Средний рост", examples=["170-180 см"]
    )
    average_weight: Optional[constr(max_length=50)] = Field(  # type: ignore
        None, description="Средний вес", examples=["60-80 кг"]
    )
    physical_features: Optional[str] = Field(
        None, max_length=1000, description="Физические особенности"
    )
    is_playable: bool = Field(default=True, description="Доступна ли раса для игроков")
    rarity: str = Field(default="обычная", description="Редкость расы в мире")
    homeland_regions: Optional[List[str]] = Field(
        default=[],
        description="Регионы происхождения",
        examples=[["Северные леса", "Эльфийское королевство"]],
    )

    @field_validator("rarity")
    def validate_rarity_field(cls, v: str) -> str:
        return validate_race_rarity(v)  # type: ignore

    @field_validator("stat_bonuses")
    def validate_stat_bonuses_field(
        cls, v: Optional[Dict[str, int]]
    ) -> Optional[Dict[str, int]]:
        return validate_stat_bonuses(v)

    @field_validator("racial_abilities")
    def validate_racial_abilities_field(
        cls, v: Optional[List[str]]
    ) -> Optional[List[str]]:
        return validate_racial_abilities(v)

    @field_validator("special_traits")
    def validate_special_traits_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=1000)

    @field_validator("physical_features")
    def validate_physical_features_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=1000)


class RaceUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=100, strip_whitespace=True)] = None  # type: ignore
    description: Optional[str] = Field(None, max_length=2000)
    size: Optional[str] = None
    racial_abilities: Optional[List[str]] = None
    stat_bonuses: Optional[Dict[str, int]] = None
    languages: Optional[List[str]] = None
    special_traits: Optional[str] = Field(None, max_length=1000)
    average_height: Optional[constr(max_length=50)] = None  # type: ignore
    average_weight: Optional[constr(max_length=50)] = None  # type: ignore
    physical_features: Optional[str] = Field(None, max_length=1000)
    is_playable: Optional[bool] = None
    rarity: Optional[str] = None
    homeland_regions: Optional[List[str]] = None

    @field_validator("size")
    def validate_size_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_race_size(v) if v is not None else None

    @field_validator("rarity")
    def validate_rarity_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_race_rarity(v) if v is not None else None

    @field_validator("stat_bonuses")
    def validate_stat_bonuses_field(
        cls, v: Optional[Dict[str, int]]
    ) -> Optional[Dict[str, int]]:
        return validate_stat_bonuses(v)

    @field_validator("racial_abilities")
    def validate_racial_abilities_field(
        cls, v: Optional[List[str]]
    ) -> Optional[List[str]]:
        return validate_racial_abilities(v)

    @field_validator("description")
    def validate_description_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=2000)

    @field_validator("special_traits")
    def validate_special_traits_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=1000)

    @field_validator("physical_features")
    def validate_physical_features_field(cls, v: Optional[str]) -> Optional[str]:
        return validate_text_field(v, max_length=1000)

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not any(getattr(self, field) is not None for field in self.model_fields):
            raise ValueError("Для обновления должно быть передано хотя бы одно поле")
        return self


class RaceResponse(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор расы")
    name: str = Field(..., description="Название расы")
    description: Optional[str] = Field(None, description="Описание расы")
    size: str = Field(..., description="Размер представителей расы")
    racial_abilities: Optional[List[str]] = Field(
        None, description="Расовые способности"
    )
    stat_bonuses: Optional[Dict[str, Any]] = Field(
        None, description="Бонусы к характеристикам"
    )
    languages: Optional[List[str]] = Field(None, description="Известные языки")
    special_traits: Optional[str] = Field(None, description="Особые черты расы")
    average_height: Optional[str] = Field(None, description="Средний рост")
    average_weight: Optional[str] = Field(None, description="Средний вес")
    physical_features: Optional[str] = Field(None, description="Физические особенности")
    is_playable: bool = Field(..., description="Доступна ли раса для игроков")
    rarity: Optional[str] = Field(..., description="Редкость расы в мире")
    homeland_regions: Optional[List[str]] = Field(
        None, description="Регионы происхождения"
    )
    created_at: datetime = Field(..., description="Дата создания записи")
    updated_at: datetime = Field(..., description="Дата последнего обновления записи")


class RaceListResponse(BaseModel):
    races: List[RaceResponse] = Field(..., description="Список рас")
    total: int = Field(..., description="Общее количество рас")
    page: int = Field(..., description="Номер страницы")
    size: int = Field(..., description="Размер страницы")
