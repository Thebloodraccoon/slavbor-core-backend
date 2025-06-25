from fastapi import HTTPException, status


class RaceNotFoundException(HTTPException):
    """Exception raised when a race is not found."""

    def __init__(self, race_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Race with id {race_id} not found",
        )


class RaceAlreadyExistsException(HTTPException):
    """Exception raised when trying to create a race that already exists."""

    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Race with name {name} already exists",
        )


class RaceRarityException(HTTPException):
    """Exception raised when rarity non readble"""

    def __init__(self, rarity: str, readable_rarities: list[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "The unacceptable value of rarity",
                "received": rarity,
                "allowed_values": readable_rarities,
                "examples": ["очень редкая", "редкая", "обычная", "очень_редкая"],
            },
        )
