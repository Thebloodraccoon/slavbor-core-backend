"""
Константы для моделей базы данных.
Содержит все возможные значения для enum-полей и constraints.
"""

# Character model constants
CHARACTER_TYPES = ["npc", "player", "historical", "deity", "legendary", "template"]

CHARACTER_STATUSES = ["alive", "dead", "missing", "legendary", "unknown"]

SOCIAL_RANKS = [
    "император",
    "король",
    "князь",
    "герцог",
    "граф",
    "боярин",
    "рыцарь",
    "дворянин",
    "торговец",
    "ремесленник",
    "крестьянин",
    "раб",
]

# Article model constants
ARTICLE_TYPES = [
    "персонаж",
    "локация",
    "фракция",
    "раса",
    "событие",
    "легенда",
    "история",
    "культура",
    "религия",
    "политика",
    "экономика",
    "военное_дело",
    "магия",
    "технология",
    "язык",
    "обычаи",
    "артефакт",
    "организация",
    "правила",
    "хроника",
    "биография",
    "географический_справочник",
    "исторический_документ",
    "законы",
    "торговые_пути",
    "генеалогия",
    "справочник",
]

ARTICLE_CATEGORIES = [
    "персонажи",
    "география",
    "история",
    "политика",
    "культура",
    "религия",
    "экономика",
    "военное_дело",
    "магия",
    "расы",
    "фракции",
    "технологии",
    "языки",
    "обычаи",
    "артефакты",
    "справочники",
    "правила_игры",
]

ARTICLE_STATUSES = ["draft", "review", "published", "archived", "deleted"]

DIFFICULTY_LEVELS = ["beginner", "easy", "medium", "hard", "expert"]

SOURCE_TYPES = [
    "original",
    "translated",
    "adapted",
    "compiled",
    "referenced",
    "player_created",
]

CANONICAL_STATUSES = ["canon", "semi_canon", "non_canon", "alternative", "disputed"]

RELIABILITY_LEVELS = [
    "verified",
    "reliable",
    "mostly_reliable",
    "questionable",
    "unreliable",
    "fictional",
]

VISIBILITY_LEVELS = ["public", "players_only", "gm_only", "private"]

# Faction model constants
FACTION_TYPES = [
    "торговая_династия",
    "военный_клан",
    "религиозная_группа",
    "дворянский_род",
    "торговая_гильдия",
    "ремесленная_гильдия",
    "военный_орден",
    "рыцарский_орден",
    "княжеский_дом",
    "королевская_династия",
    "императорский_дом",
    "племенной_союз",
    "городское_правительство",
    "республика",
    "тайное_общество",
    "культ",
    "секта",
    "братство",
    "пиратская_флотилия",
    "разбойничья_банда",
    "наемная_компания",
]

FACTION_STATUSES = [
    "зарождающаяся",
    "растущая",
    "активная",
    "могущественная",
    "доминирующая",
    "стабильная",
    "в_упадке",
    "ослабленная",
    "разрушающаяся",
    "разрушенная",
    "историческая",
    "легендарная",
]

LEADERSHIP_TYPES = [
    "наследственная",
    "выборная",
    "военная",
    "теократическая",
    "олигархическая",
    "диктаторская",
    "коллективная",
]

POWER_LEVELS = [
    "отсутствует",
    "минимальная",
    "слабая",
    "средняя",
    "сильная",
    "очень_сильная",
    "доминирующая",
]

HISTORICAL_IMPORTANCE_LEVELS = [
    "незначительная",
    "местная",
    "региональная",
    "национальная",
    "международная",
    "легендарная",
]

# Location model constants
LOCATION_TYPES = [
    "континент",
    "страна",
    "регион",
    "княжество",
    "провинция",
    "город",
    "столица",
    "деревня",
    "поселок",
    "хутор",
    "крепость",
    "замок",
    "форт",
    "застава",
    "храм",
    "монастырь",
    "святилище",
    "руины",
    "развалины",
    "древний_город",
    "порт",
    "пристань",
    "переправа",
    "дорога",
    "торговый_путь",
    "перевал",
    "лес",
    "роща",
    "болото",
    "пустыня",
    "горы",
    "река",
    "озеро",
    "море",
    "залив",
]

LOCATION_STATUSES = [
    "процветающая",
    "активная",
    "стабильная",
    "в_упадке",
    "заброшенная",
    "руины",
    "разрушенная",
]

FORTIFICATION_LEVELS = [
    "открытая",
    "частично_укрепленная",
    "укрепленная",
    "крепость",
    "неприступная_крепость",
]

STRATEGIC_IMPORTANCE_LEVELS = [
    "незначительная",
    "низкая",
    "средняя",
    "высокая",
    "критическая",
]

DANGER_LEVELS = [
    "очень_безопасная",
    "безопасная",
    "относительно_безопасная",
    "опасная",
    "очень_опасная",
    "смертельная",
]

# Race model constants
RACE_SIZES = ["Крошечный", "Маленький", "Средний", "Большой", "Огромный", "Гигантский"]

RACE_RARITIES = ["очень_редкая", "редкая", "необычная", "обычная", "распространенная"]

# User model constants
USER_ROLES = ["found_father", "keeper", "player"]

# Shared wealth levels (used by multiple models)
WEALTH_LEVELS = ["нищий", "бедный", "средний", "богатый", "очень_богатый"]

ENTITY_WEALTH_LEVELS = [
    "нищая",
    "бедная",
    "скромная",
    "средняя",
    "богатая",
    "очень_богатая",
    "баснословно_богатая",
]


def create_enum_constraint(field_name: str, values: list, nullable: bool = True) -> str:
    """Creates a line for CheckContraint with ENUM values."""
    values_str = ", ".join(repr(v) for v in values)

    if nullable:
        return f"{field_name} IS NULL OR {field_name} IN ({values_str})"
    else:
        return f"{field_name} IN ({values_str})"


def create_range_constraint(
    field_name: str, min_val: int, max_val: int, nullable: bool = True
) -> str:
    """Creates a line for CheckContraint with a numerical range."""
    constraint = f"({field_name} >= {min_val} AND {field_name} <= {max_val})"

    if nullable:
        return f"{field_name} IS NULL OR {constraint}"
    else:
        return constraint
