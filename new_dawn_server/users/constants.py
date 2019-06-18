from enum import Enum

class UserReviewStatus(Enum):
    PENDING = 0
    BLOCK = 1
    NORMAL = 2
    GOOD = 3
    PROMOTE = 4
