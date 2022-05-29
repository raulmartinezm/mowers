"""Application models."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from src.seat_code_mowers.exceptions import InvalidMovementError


BOTTOM_LEFT_X_COORDINATE = 0
BOTTOM_LEFT_Y_COORDINATE = 0


class Movement(str, Enum):
    """Possible movements."""

    LEFT_90_DEGREES = "L"
    RIGHT_90_DEGREES = "R"
    MOVE_FORWARD = "M"


class Heading(str, Enum):
    """Possible heading."""

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    @property
    def is_horizontal(self):
        """Returns True if the heading is horizontal or false if not."""
        return self is Heading.EAST or self is Heading.WEST

    @property
    def is_vertical(self):
        """Returns True if the heading is vertical or false if not."""
        return self is Heading.NORTH or self is Heading.SOUTH


@dataclass(unsafe_hash=True)
class Coordinates:
    """Represents a location in space."""

    x: int
    y: int

    def __post_init__(self):
        """Post init checks."""
        if not type(self.x) is int or not type(self.y) is int:
            raise ValueError(f"Invalid coordinates '({self.x}, {self.y})'")


def calculate_heading(current_heading: Heading, movement: Movement) -> Heading:
    """Calculates the new heading for a given movement."""
    if movement == Movement.MOVE_FORWARD:
        return current_heading

    elif movement == Movement.RIGHT_90_DEGREES:
        rotation = {
            Heading.NORTH: Heading.EAST,
            Heading.EAST: Heading.SOUTH,
            Heading.SOUTH: Heading.WEST,
            Heading.WEST: Heading.NORTH,
        }
    else:  # left rotation
        rotation = {
            Heading.NORTH: Heading.WEST,
            Heading.EAST: Heading.NORTH,
            Heading.SOUTH: Heading.EAST,
            Heading.WEST: Heading.SOUTH,
        }
    return rotation[current_heading]


class Plateau:
    """Representation of a plateau."""

    def __init__(self, upper_right_x: int, upper_right_y: int):
        """Initialize plateau with the upper-right coordinates.

        Args:
            upper_right_x: Upper-right X coordinates of the plateau.
            upper_right_y: Upper-right Y coordinates of the plateau.
        """
        self._upper_right_x = upper_right_x
        self._upper_right_y = upper_right_y
        self._coordinates = dict()

    def add_mower(self, mower: Mower):
        """Add a mower to the plateau.

        Args:
            mower: The mower.
        """
        self._coordinates[mower.location] = mower

    def calculate_new_position_after_forward_movement(
        self, current_position: Coordinates, heading: Heading
    ) -> Coordinates:
        """Calculate a new position given current position and heading.

        Args:
            current_position: The current coordinates.
            heading: The current heading.

        Returns:
            The new coordinates.

        Raises:
            InvalidMovementError: When it can't move with that heading.
        """
        coordinates = self._calculate_new_position(current_position, heading)
        self._check_new_position_validity(coordinates)
        self._save_new_position_of_mower(coordinates, current_position)

        return coordinates

    def _save_new_position_of_mower(self, coordinates, current_position):
        self._coordinates[coordinates] = self._coordinates[current_position]
        del self._coordinates[current_position]

    def _check_new_position_validity(self, coordinates):
        if not self._is_inside_plateau(coordinates):
            raise InvalidMovementError(f"'{coordinates}' out of plateau")
        if coordinates in self._coordinates:
            raise InvalidMovementError(f"'{coordinates}' already occupied")

    @staticmethod
    def _calculate_new_position(current_position, heading):
        step = 1 if Plateau._is_incremental_heading(heading) else -1

        if heading.is_vertical:
            coordinates = Coordinates(current_position.x, current_position.y + step)
        else:
            coordinates = Coordinates(current_position.x + step, current_position.y)
        return coordinates

    def _is_inside_plateau(self, coordinates):
        return (
            BOTTOM_LEFT_X_COORDINATE <= coordinates.x <= self._upper_right_x
            and BOTTOM_LEFT_Y_COORDINATE <= coordinates.y <= self._upper_right_y
        )

    @staticmethod
    def _is_incremental_heading(heading: Heading) -> bool:
        """Tells if moving in an axe is incremental or decremental.

        The bottom-left coordinates are assumed to be 0, 0, so moving forward
        increments Y when heading north and decrements when heading south.
        For X axe heading east increments and west decrements.

        Args:
            heading: The current heading.

        Returns:
            True for increment, False for decrement.
        """
        return heading == Heading.NORTH or heading == heading.EAST


@dataclass
class Mower:
    """Represents a Mower."""

    id: UUID
    location: Coordinates
    heading: Heading
    plateau: Plateau

    def __post_init__(self):  # noqa: D105
        self.plateau.add_mower(self)

    def move(self, movement: Movement) -> None:
        """Move the Mower to a new position.

        Args:
            movement: The kind of movement to perform.

        Raises:
            InvalidMovementError: When it can't move with that heading.
        """
        if movement is Movement.MOVE_FORWARD:
            try:
                self.location = (
                    self.plateau.calculate_new_position_after_forward_movement(
                        self.location, self.heading
                    )
                )
            except InvalidMovementError:
                raise
        else:
            self.heading = calculate_heading(self.heading, movement)
