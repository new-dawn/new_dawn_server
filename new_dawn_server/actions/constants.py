from enum import Enum

END_USER_FIRSTNAME = "end_user_first_name"
END_USER_LASTNAME = "end_user_last_name"
END_USER_ID = "end_user_id"
END_USER_IMAGE_URL = "end_user_image_url"
LAST_UPDATE_TIME = "last_update_time"
MESSAGES = "messages"

class ActionType(Enum):
    LIKE = 1
    BLOCK = 2
    MATCH = 3
    RELATIONSHIP = 4
    MESSAGE = 5
    REQUEST_TAKEN = 6
    UNMATCH = 7
    ACCEPT_TAKEN = 8
    ALREADY_TAKEN = 9
    UNTAKEN = 10

class EntityType(Enum):
    NONE = 0
    MAIN_IMAGE = 1
    BASIC_INFO = 2
    QUESTION_ANSWER = 3
