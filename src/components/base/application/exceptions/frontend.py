from fastapi import HTTPException


class FrontendException(HTTPException):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(detail=message, status_code=status_code)
