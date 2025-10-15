from models.gender_enum import Gender
import pytest

def test_parse_gender_with_enum():
    assert Gender.parse_gender(Gender.MAN) == Gender.MAN
    assert Gender.parse_gender(Gender.WOMAN) == Gender.WOMAN

def test_parse_gender_with_int():
    assert Gender.parse_gender(1) == Gender.MAN
    assert Gender.parse_gender(2) == Gender.WOMAN
    with pytest.raises(ValueError):
        Gender.parse_gender(3)

def test_parse_gender_with_string():
    assert Gender.parse_gender("man") == Gender.MAN
    assert Gender.parse_gender("WOMAN") == Gender.WOMAN
    assert Gender.parse_gender("Man") == Gender.MAN
    with pytest.raises(ValueError):
        Gender.parse_gender("other")

def test_parse_gender_invalid_type():
    with pytest.raises(ValueError):
        Gender.parse_gender(5.5)
    with pytest.raises(ValueError):
        Gender.parse_gender(None)
    with pytest.raises(ValueError):
        Gender.parse_gender([])
