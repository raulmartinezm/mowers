"""This file contains the custom exceptions used in the project."""


class MowerBaseError(Exception):
    """Base exception."""

    pass


class InvalidMovementError(MowerBaseError):
    """The Mower can't move to the given position."""

    pass


class MowerNotFoundError(MowerBaseError):
    """The mower can't be found."""

    pass


class InvalidInputError(MowerBaseError):
    """The input cannot be processed."""

    pass
