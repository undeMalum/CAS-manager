from enum import Enum, auto


class AddMode(Enum):
    """Holds modes of the Adding Frame"""
    UPDATE_CLASS = auto()
    NEW_CLASS = auto()
    NEW_STUDENT = auto()
