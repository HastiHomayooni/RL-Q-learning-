
import pytest
import sys
from unittest.mock import patch

# Importing functions
from project import create_dic, get_user_input, validate_input_format


# Test for create_dic function
def test_create_dic():
    action_rate = 0.7
    comedy_rate = 0.3
    drama_rate = 0.4
    result = create_dic(action_rate, comedy_rate, drama_rate)

    expected = {
        "Action": 0.7,
        "Comedy": 0.3,
        "Drama": 0.4
    }

    assert result == expected, f"Expected {expected}, but got {result}"


# Test for validate_input_format function
def test_validate_input_format_valid():
    valid_input = "User1-0.7-0.3-0.4"
    result = validate_input_format(valid_input)

    expected = ["User1", "0.7", "0.3", "0.4"]

    assert result == expected, f"Expected {expected}, but got {result}"

def test_validate_input_format_invalid():
    invalid_input = "User1-0.7-1.3-0.4"  # Invalid format (out of range)

    with pytest.raises(SystemExit):
        validate_input_format(invalid_input)


# Test for get_user_input function
@patch('builtins.input', side_effect=["User1-0.7-0.3-0.4", "done"])
def test_get_user_input(mock_input):
    result = get_user_input()

    expected = ["User1-0.7-0.3-0.4"]

    assert result == expected, f"Expected {expected}, but got {result}"
