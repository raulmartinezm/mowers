"""Tests for services of Mowers challenge."""
from uuid import UUID

import pytest
from src.seat_code_mowers.exceptions import MowerNotFoundError
from src.seat_code_mowers.service import MowerService


def test_mower_service_creates_a_mower_ok(mocker):
    """It creates a mower and returns its identifier."""
    mocker.patch(
        "src.seat_code_mowers.service.uuid.uuid4",
        return_value=UUID("a4b58329-ac0d-4c79-a6cb-794d92f6ab66"),
    )
    mower_service = MowerService()
    mower_id = mower_service.create_mower(
        heading="N", coordinates=(0, 0), plateau=(5, 5)
    )

    assert mower_id == "a4b58329-ac0d-4c79-a6cb-794d92f6ab66"


@pytest.mark.parametrize(
    "heading, coordinates, plateau",
    [("", (0, 0), (5, 5)), ("N", ("", 0), (5, 5)), ("", (0, 0), (5, ""))],
)
def test_mower_service_raises_exception_when_missing_params(
    heading, coordinates, plateau
):
    """It raises an exception for invalid attributes."""
    mower_service = MowerService()
    with pytest.raises(ValueError):
        mower_service.create_mower(heading, coordinates, plateau)


def test_send_instructions_to_mower():
    """It sends the instructions for exploring the plateau."""
    mower_service = MowerService()
    mower_id = mower_service.create_mower(
        heading="N", coordinates=(1, 2), plateau=(5, 5)
    )

    mower_service.send_instructions(mower_id, "LMLMLMLMM")
    mower_state = mower_service.get_mower_status(mower_id)

    assert mower_state == "1 3 N"


def test_get_mower_status_after_create_ok():
    """It returns the status of a Mower that hasn't moved yet."""
    mower_service = MowerService()
    mower_id = mower_service.create_mower(
        heading="N", coordinates=(1, 2), plateau=(5, 5)
    )
    mower_state = mower_service.get_mower_status(mower_id)

    assert mower_state == "1 2 N"


def test_when_sending_instructions_to_mower_not_found_it_should_raise_an_exception():
    """It raises an exception when trying to send instructions to non existing Mower."""
    mower_service = MowerService()
    with pytest.raises(MowerNotFoundError):
        mower_service.send_instructions(
            "7d558c83-abbc-4614-8832-8b2b452f9288", "LMLMLMLMM"
        )


def test_when_getting_status_from_mower_not_found_it_should_raise_an_exception():
    """It raises an exception when trying to get the status from non existing Mower."""
    mower_service = MowerService()

    with pytest.raises(MowerNotFoundError):
        mower_service.get_mower_status("7d558c83-abbc-4614-8832-8b2b452f9288")
