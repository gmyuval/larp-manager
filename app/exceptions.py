from fastapi import HTTPException


class PlayerAlreadyExists(HTTPException):
    def __init__(self, detail: str = "Player already exists"):
        super().__init__(status_code=409, detail=detail)