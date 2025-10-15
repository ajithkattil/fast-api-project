from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class GoneException(HTTPException):
    def __init__(self, detail: str = "Resource no longer available"):
        super().__init__(status_code=status.HTTP_410_GONE, detail=detail)


class InternalException(HTTPException):
    def __init__(self, detail: str = "Internal Server"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class AccessDeniedException(HTTPException):
    def __init__(self, detail: str = "Access Denied"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UnprocessableException(HTTPException):
    def __init__(self, detail: str = "Unprocessable Entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class ServerError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class RecipeNotFoundError(ValueError):
    """Recipe does not exist - data/request error"""

    def __init__(self, message: str, recipe_id: str | int | None = None):
        super().__init__(message)
        self.recipe_id = None
        if recipe_id:
            if isinstance(recipe_id, int):
                self.recipe_id = str(recipe_id)
            else:
                self.recipe_id = recipe_id


class RecipeAlreadyDeletedError(ValueError):
    """Recipe is already marked as deleted - data/request error"""

    def __init__(self, message: str, recipe_id: str | int | None = None):
        super().__init__(message)
        self.recipe_id = None
        if recipe_id:
            if isinstance(recipe_id, int):
                self.recipe_id = str(recipe_id)
            else:
                self.recipe_id = recipe_id


class OrderNotFoundError(ValueError):
    """Order not found - data/request error"""

    pass
