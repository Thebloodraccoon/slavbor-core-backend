from typing import Dict, List, Optional

from app.constants import RACE_RARITIES, RACE_SIZES


def validate_race_size(v: Optional[str]) -> Optional[str]:
    """Validation of race size."""
    if v and v not in RACE_SIZES:
        raise ValueError(f'Размер должен быть одним из: {", ".join(RACE_SIZES)}')
    return v


def validate_race_rarity(v: Optional[str]) -> Optional[str]:
    """Validation of race rarity."""
    if v and v not in RACE_RARITIES:
        raise ValueError(f'Редкость должна быть одной из: {", ".join(RACE_RARITIES)}')
    return v


def validate_stat_bonuses(v: Optional[Dict[str, int]]) -> Optional[Dict[str, int]]:
    """Validation of D&D stat bonuses."""
    if not v:
        return v

    valid_stats = {
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    }

    for stat, bonus in v.items():
        if stat.lower() not in valid_stats:
            raise ValueError(
                f'Неизвестная характеристика: {stat}. Допустимые: {", ".join(valid_stats)}'
            )
        if not isinstance(bonus, int) or bonus < -5 or bonus > 5:
            raise ValueError(
                f"Бонус характеристики должен быть целым числом от -5 до 5, получено: {bonus}"
            )

    return v


def validate_racial_abilities(v: Optional[List[str]]) -> Optional[List[str]]:
    """Validation of racial abilities list."""
    if not v:
        return v

    if len(v) > 10:
        raise ValueError("Слишком много расовых способностей (максимум 10)")

    for ability in v:
        if not ability or len(ability.strip()) < 3:
            raise ValueError("Название способности должно содержать минимум 3 символа")

    return v


def validate_name_field(
    v: Optional[str], min_length: int = 2, max_length: int = 100
) -> Optional[str]:
    """Validation of name/title field."""
    if v is None:
        return v

    v = v.strip()
    if len(v) < min_length:
        raise ValueError(f"Название должно содержать минимум {min_length} символа")
    if len(v) > max_length:
        raise ValueError(f"Название не должно превышать {max_length} символов")

    return v


def validate_text_field(v: Optional[str], max_length: int = 2000) -> Optional[str]:
    """Validation of text field with length restriction."""
    if v is None:
        return v

    if len(v) > max_length:
        raise ValueError(f"Текст не должен превышать {max_length} символов")

    return v


def validate_list_not_empty(
    v: Optional[List], field_name: str = "список"
) -> Optional[List]:
    """Validation that list is not empty if provided."""
    if v is not None and len(v) == 0:
        raise ValueError(f"{field_name} не может быть пустым")
    return v


def validate_at_least_one_field(data: dict, field_names: List[str]) -> dict:
    """Validation that at least one field is provided for update."""
    if not any(data.get(field) is not None for field in field_names):
        raise ValueError("Для обновления должно быть передано хотя бы одно поле")
    return data
