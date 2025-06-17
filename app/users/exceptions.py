from typing import Optional

from fastapi import HTTPException, status

class UserNotFoundException(HTTPException):
    def init(self, user_id: Optional[int] = None, email: Optional[str] = None):
        detail = "404 User is not found"

        if user_id:
            detail = f"404 User with ID {user_id} is not found."

        if email:
            detail = f"404 User with email {email} is not found."

        super().init(status_code=status.HTTP_404_NOT_FOUND, detail=detail)