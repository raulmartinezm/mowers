"""Tests for the domain module."""
import uuid

import pytest
from src.seat_code_mowers.domain import Coordinates
from src.seat_code_mowers.domain import Heading
from src.seat_code_mowers.domain import Movement
from src.seat_code_mowers.domain import Mower
from src.seat_code_mowers.domain import Plateau
from src.seat_code_mowers.exceptions import InvalidMovementError


def test_create_coordinates_with_correct_values():
    """It creates a coordinates object with its attributes."""
    coordinates = Coordinates(4, 3)

    assert coordinates.x == 4
    assert coordinates.y == 3


def test_create_coordinates_with_invalid_values_raises_an_error():
    """It raises an error for invalid coordinates."""
    with pytest.raises(ValueError) as aer:
        Coordinates(4, "a")

    assert aer.value.args[0] == "Invalid coordinates '(4, a)'"


def test_heading_enum_vertical_values_should_be_correct():
    """Heading north or south implies vertical movement."""
    assert Heading.NORTH.is_vertical
    assert Heading.SOUTH.is_vertical
    assert not Heading.EAST.is_vertical
    assert not Heading.WEST.is_vertical


def test_heading_enum_horizontal_values_should_be_correct():
    """Heading east or west implies horizontal movement."""
    assert not Heading.NORTH.is_horizontal
    assert not Heading.SOUTH.is_horizontal
    assert Heading.EAST.is_horizontal
    assert Heading.WEST.is_horizontal


def test_when_create_a_mower_it_has_the_expected_values():
    """It creates a Mower and check its attributes."""
    start_position = Coordinates(0, 0)
    mower_id = uuid.UUID("a4b58329-ac0d-4c79-a6cb-794d92f6ab66")

    mower = Mower(
        mower_id,
        start_position,
        Heading.NORTH,
        Plateau(5, 5),
    )

    assert mower.location == Coordinates(0, 0)
    assert mower.heading == Heading.NORTH
    assert mower.plateau
    assert mower.id == mower_id


def test_a_mower_can_move_forward():
    """It moves forwards 1 position."""
    start_position = Coordinates(0, 0)
    mower = Mower(
        uuid.uuid4(),
        start_position,
        Heading.NORTH,
        Plateau(upper_right_x=5, upper_right_y=5),
    )

    mower.move(Movement.MOVE_FORWARD)

    assert mower.location == Coordinates(0, 1)
    assert mower.heading == Heading.NORTH


@pytest.mark.parametrize(
    "start_heading, expected_heading",
    [
        (Heading.NORTH, Heading.WEST),
        (Heading.EAST, Heading.NORTH),
        (Heading.SOUTH, Heading.EAST),
        (Heading.WEST, Heading.SOUTH),
    ],
)
def test_when_a_mower_can_rotates_90_degrees_left_the_heading_is_correct(
    start_heading, expected_heading
):
    """It rotates 90 degrees left."""
    start_position = Coordinates(0, 0)
    mower = Mower(
        uuid.uuid4(),
        start_position,
        start_heading,
        Plateau(upper_right_x=5, upper_right_y=5),
    )

    mower.move(Movement.LEFT_90_DEGREES)

    assert mower.location == start_position
    assert mower.heading == expected_heading


@pytest.mark.parametrize(
    "start_heading, expected_heading",
    [
        (Heading.NORTH, Heading.EAST),
        (Heading.EAST, Heading.SOUTH),
        (Heading.SOUTH, Heading.WEST),
        (Heading.WEST, Heading.NORTH),
    ],
)
def test_when_a_mower_can_rotates_90_degrees_right_the_heading_is_correct(
    start_heading, expected_heading
):
    """It rotates 90 degrees right."""
    start_position = Coordinates(0, 0)
    mower = Mower(
        uuid.uuid4(),
        start_position,
        start_heading,
        Plateau(upper_right_x=5, upper_right_y=5),
    )

    mower.move(Movement.RIGHT_90_DEGREES)

    assert mower.location == start_position
    assert mower.heading == expected_heading


@pytest.mark.parametrize(
    "position, heading, expected_message",
    [
        (
            Coordinates(0, 0),
            Heading.SOUTH,
            "'Coordinates(x=0, y=-1)' out of plateau",
        ),
        (
            Coordinates(0, 0),
            Heading.WEST,
            "'Coordinates(x=-1, y=0)' out of plateau",
        ),
        (
            Coordinates(5, 5),
            Heading.NORTH,
            "'Coordinates(x=5, y=6)' out of plateau",
        ),
    ],
)
def test_an_invalid_movement_raises_an_exception(position, heading, expected_message):
    """It raises an exception when trying to move out from plateau."""
    mower = Mower(
        uuid.uuid4(), position, heading, Plateau(upper_right_x=5, upper_right_y=5)
    )

    with pytest.raises(InvalidMovementError) as exim:
        mower.move(Movement.MOVE_FORWARD)

    assert exim.value.args[0] == expected_message


def test_a_mower_can_be_moved_to_a_free_position():
    """It moves to a free position."""
    plateau = Plateau(upper_right_x=5, upper_right_y=5)

    Mower(uuid.uuid4(), Coordinates(2, 3), Heading.NORTH, plateau)
    mower = Mower(uuid.uuid4(), Coordinates(1, 1), Heading.NORTH, plateau)
    mower.move(Movement.MOVE_FORWARD)

    assert mower.location.x == 1
    assert mower.location.y == 2


def test_a_mower_can_be_moved_to_the_previous_position_of_another():
    """It moves to a recently freed position."""
    plateau = Plateau(upper_right_x=5, upper_right_y=5)

    mower1 = Mower(uuid.uuid4(), Coordinates(2, 3), Heading.NORTH, plateau)
    mower1.move(Movement.MOVE_FORWARD)

    mower2 = Mower(uuid.uuid4(), Coordinates(2, 2), Heading.NORTH, plateau)
    mower2.move(Movement.MOVE_FORWARD)

    assert mower1.location.x == 2
    assert mower1.location.y == 4

    assert mower2.location.x == 2
    assert mower2.location.y == 3


def test_a_mower_cannot_be_moved_to_a_occupied_position():
    """It raises an exception when trying to move into another mower's position."""
    plateau = Plateau(upper_right_x=5, upper_right_y=5)

    Mower(uuid.uuid4(), Coordinates(2, 3), Heading.NORTH, plateau)

    mower = Mower(uuid.uuid4(), Coordinates(2, 2), Heading.NORTH, plateau)

    with pytest.raises(InvalidMovementError) as exim:
        mower.move(Movement.MOVE_FORWARD)

    assert exim.value.args[0] == "'Coordinates(x=2, y=3)' already occupied"
