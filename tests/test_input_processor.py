"""Tests for input module."""
import pytest
from src.seat_code_mowers.exceptions import InvalidInputError
from src.seat_code_mowers.input_processor import process_input


@pytest.mark.parametrize(
    "mowers_input, expected_output",
    [
        (
            "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n",
            "1 3 N\n5 1 E\n",
        )
    ],
)
def test_it_can_read_a_valid_input(mowers_input, expected_output):
    """It reads the input and produces the expected output."""
    output = process_input(mowers_input)
    assert output.strip() == expected_output.strip()


@pytest.mark.parametrize(
    "mowers_input",
    ["", "asdasd", "5 5\n12312", "5 5\n1 2 3\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM\n"],
)
def test_when_read_an_invalid_input_it_raises_an_exception(mowers_input):
    """It raises an exception when it cannot process the input."""
    with pytest.raises(InvalidInputError):
        process_input(mowers_input)
