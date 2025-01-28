from fastapi import HTTPException


class PlayerAlreadyExists(HTTPException):
    def __init__(self, detail: str = "Player already exists"):
        super().__init__(status_code=409, detail=detail)


class PlayerNotFound(HTTPException):
    def __init__(self, detail: str = "Player not found"):
        super().__init__(status_code=404, detail=detail)


class BadId(HTTPException):
    def __init__(self, detail: str = "ID in request is not a valid UUID"):
        super().__init__(status_code=400, detail=detail)
