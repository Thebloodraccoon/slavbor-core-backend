from app.constants import RACE_RARITIES
from app.exceptions.race_exceptions import RaceRarityException


def normalize_rarity(rarity: str) -> str:
    """
    Normalizes the Rarity parameter:
    - leads to the lower register
    - replaces gaps for emphasis
    - Checks validity
    """
    normalized = rarity.lower().replace(" ", "_").replace("-", "_")

    if normalized not in RACE_RARITIES:
        readable_rarities = [r.replace("_", " ") for r in RACE_RARITIES]
        raise RaceRarityException(rarity, readable_rarities)

    return normalized
