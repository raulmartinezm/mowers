"""Input processor module."""
from typing import Tuple

from src.seat_code_mowers.exceptions import InvalidInputError
from src.seat_code_mowers.service import MowerService


def process_input(mowers_input: str) -> str:
    """Process the instructions for the Mowers."""
    lines = [lines.strip() for lines in mowers_input.split("\n") if lines]

    if not lines:
        raise InvalidInputError(f"Unprocessable input: {mowers_input}")

    try:
        upper_right_coords = tuple(int(coord) for coord in lines.pop(0).split(" "))

        mowers = [lines[i : i + 2] for i in range(0, len(lines), 2)]
    except ValueError as verr:
        raise InvalidInputError(f"Unprocessable input: {mowers_input}") from verr

    mower_service = MowerService()

    output = ""

    for mower in mowers:
        try:
            coords = _extract_mower_coords(mower[0])
            heading = _extract_mower_heading(mower[0])
            mower_id = mower_service.create_mower(heading, coords, upper_right_coords)
        except (IndexError, ValueError) as ex:
            raise InvalidInputError(f"Unprocessable input: {mowers_input}") from ex

        mower_service.send_instructions(mower_id, mower[1])
        output += mower_service.get_mower_status(mower_id) + "\n"

    return output


def _extract_mower_coords(mower: str) -> Tuple:
    coords = [elem for elem in mower.split(" ") if elem]
    coords.pop()
    return tuple(int(elem) for elem in coords)


def _extract_mower_heading(mower: str) -> str:
    return [elem for elem in mower.split(" ") if elem][2]
