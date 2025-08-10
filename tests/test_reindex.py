import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from reindex_elasticsearch import parse_index_range, validate_index_name

def test_validate_index_name_valid():
    assert validate_index_name('fg-000001') is True
    assert validate_index_name('adc-123456') is True

def test_validate_index_name_invalid():
    assert validate_index_name('fg-12345') is False       # меньше 6 цифр
    assert validate_index_name('fg123456') is False       # нет дефиса
    assert validate_index_name('fg-abcdef') is False      # не цифры
    assert validate_index_name('fg-1234567') is False     # больше 6 цифр

def test_parse_index_range_valid():
    result = parse_index_range('fg-000001', 'fg-000003')
    assert result == ['fg-000001', 'fg-000002', 'fg-000003']

def test_parse_index_range_invalid_prefix():
    with pytest.raises(ValueError):
        parse_index_range('fg-000005', 'abc-000010')

def test_parse_index_range_start_greater_than_end():
    with pytest.raises(ValueError):
        parse_index_range('fg-000010', 'fg-000005')

def test_parse_index_range_bad_format():
    with pytest.raises(ValueError):
        parse_index_range('fg000001', 'fg000005')
