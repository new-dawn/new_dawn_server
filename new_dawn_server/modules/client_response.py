# An object for unifying client response
# with support for formating and auto-logging

from typing import Dict

class ClientResponse:

    def __init__(self, success: bool, message: str, log: bool=False) -> None:
        self.success = success
        self.message = message
        self.log = log

    def get_response_as_dict(self) -> Dict[str, str]:
        if self.log:
            self.log_response(str(self.__dict__))
        return self.__dict__

    def log_response(self, msg: str) -> None:
        # TODO: use logger to print response messages
        print(msg)
