import pytest

from app.exceptions.race_exceptions import RaceRarityException
from app.races.utils import normalize_rarity


def test_normalize_rarity_valid_lowercase():
    """Test normalizing valid rarity in lowercase"""
    result = normalize_rarity("обычная")

    assert result == "обычная"


def test_normalize_rarity_valid_with_spaces():
    """Test normalizing valid rarity with spaces"""
    result = normalize_rarity("очень редкая")

    assert result == "очень_редкая"


def test_normalize_rarity_valid_with_dashes():
    """Test normalizing valid rarity with dashes"""
    result = normalize_rarity("очень-редкая")

    assert result == "очень_редкая"


def test_normalize_rarity_valid_mixed_case():
    """Test normalizing valid rarity with mixed case"""
    result = normalize_rarity("РЕДКАЯ")

    assert result == "редкая"


def test_normalize_rarity_valid_underscore():
    """Test normalizing valid rarity already with underscores"""
    result = normalize_rarity("очень_редкая")

    assert result == "очень_редкая"


def test_normalize_rarity_invalid():
    """Test normalizing invalid rarity raises exception"""
    with pytest.raises(RaceRarityException) as exc_info:
        normalize_rarity("invalid_rarity")

    assert exc_info.value.status_code == 400
    assert "The unacceptable value of rarity" in str(exc_info.value.detail)


def test_normalize_rarity_empty_string():
    """Test normalizing empty string raises exception"""
    with pytest.raises(RaceRarityException):
        normalize_rarity("")


def test_normalize_rarity_exception_details():
    """Test that exception contains proper details"""
    with pytest.raises(RaceRarityException) as exc_info:
        normalize_rarity("wrong_rarity")

    detail = exc_info.value.detail
    assert isinstance(detail, dict)
    assert "message" in detail
    assert "received" in detail
    assert "allowed_values" in detail
    assert "examples" in detail
    assert detail["received"] == "wrong_rarity"
