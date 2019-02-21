from enum import Enum


class ActionType(Enum):
    LIKE = 1
    BLOCK = 2
    MATCH = 3
    RELATIONSHIP = 4
    MESSAGE = 5


class EntityType(Enum):
    NONE = 0
    MAIN_IMAGE = 1
    BASIC_INFO = 2
    QUESTION_ANSWER = 3
