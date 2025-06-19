from fastapi import HTTPException
from starlette import status

class Error401(HTTPException):
    def __init__(self, message = "Could not validate credentials"):
        self.message = message
        super().__init__(status_code = status.HTTP_401_UNAUTHORIZED, detail = message)

    def __str__(self):
        return f"Error401: {self.message}"