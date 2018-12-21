from typing import Any, Dict

class ClientResponse:
    '''
    An class for unifying client response with support for formating and logging
    A valid client response must include "success" field and "message" field
    Other fields can be passed via kwargs
    '''
    def __init__(
            self, success: bool, message: str, log: bool=False, **kwargs) -> None:
        self.success = success
        self.message = message
        self.log = log
        self.kwargs = kwargs

    def get_response_as_dict(self) -> Dict[str, Any]:
        response: Dict[str, Any] = {
            "success": self.success,
            "message": self.message,
            **self.kwargs
        }
        if self.log:
            self.log_response(str(response))
        return response

    def log_response(self, msg: str) -> None:
        # TODO: use logger to print response messages
        print(msg)
