from enum import Enum, auto


class AddMode(Enum):
    """Holds modes of the Adding Frame"""
    UPDATE_CLASS = auto()
    NEW_CLASS = auto()
    UPDATE_STUDENT = auto()
    NEW_STUDENT = auto()
