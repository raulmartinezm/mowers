"""Application service."""
import logging
import uuid
from typing import Tuple

from src.seat_code_mowers.domain import Coordinates
from src.seat_code_mowers.domain import Heading
from src.seat_code_mowers.domain import Movement
from src.seat_code_mowers.domain import Mower
from src.seat_code_mowers.domain import Plateau
from src.seat_code_mowers.exceptions import MowerNotFoundError


logger = logging.getLogger(__name__)


class MowerService:
    """Mowers service."""

    def __init__(self):
        """Mowers service initializer."""
        self._mowers = {}

    def create_mower(self, heading: str, coordinates: Tuple, plateau: Tuple) -> str:
        """Creates a new mower.

        Args:
            heading: The initial heading.
            coordinates: The initial location of the Mower.
            plateau: The upper-right coordinates of the plateau.

        Returns:
            An ID for the Mower.
        """
        mower_heading = Heading(heading)

        self._validate_coordinates(coordinates)
        self._validate_coordinates(plateau)

        mower_id = uuid.uuid4()
        self._mowers[mower_id] = Mower(
            mower_id,
            Coordinates(coordinates[0], coordinates[1]),
            mower_heading,
            Plateau(plateau[0], plateau[1]),
        )

        return str(mower_id)

    @staticmethod
    def _validate_coordinates(coordinates: Tuple) -> None:
        if not type(coordinates) is tuple or not len(coordinates) == 2:
            raise ValueError(f"Invalid coordinates '{coordinates}'")

    def send_instructions(self, mower_id: str, instructions: str) -> None:
        """Make a Mower follow a path.

        The possible letters are “L”, “R” and ”M”. “L” and “R” make the mower
        spin 90 degrees left or right respectively, without moving from its
        current spot. “M” means to move forward one grid point and maintain
        the same Heading. ie: "LMLMLMLMM"

        Args:
            mower_id: The id of the Mower.
            instructions: The instructions to follow.

        Raises: # noqa: DAR402
            MowerNotFoundError: When it can't found a Mower by its id.
        """
        mower = self._get_mower(mower_id)

        for instruction in instructions:
            logger.debug(f"Sending Mower '{mower_id}' instruction '{instruction}'")
            mower.move(Movement(instruction))

    def _get_mower(self, mower_id) -> Mower:
        try:
            mower = self._mowers.get(uuid.UUID(mower_id))
        except ValueError as ex:
            raise MowerNotFoundError(f"Invalid Mower id '{mower_id}'") from ex

        if not mower:
            raise MowerNotFoundError(f"Mower with id '{mower_id}' not found")

        return mower

    def get_mower_status(self, mower_id: str) -> str:
        """Get the status of a Mower.

        A Mower status is a line that represents its position. Two numbers and a
        letter (heading) sepparated by spaces ie: 1 2 N

        Args:
            mower_id: The ID of the mower

        Returns:
            The status of the Mower (its position).

        Raises: # noqa: DAR402
            MowerNotFoundError: When it can't found a Mower by its id.
        """
        mower = self._get_mower(mower_id)

        return f"{mower.location.x} {mower.location.y} {mower.heading}"
