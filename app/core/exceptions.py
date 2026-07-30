class AppException(Exception):

    def __init__(self, status_code: int, detail: str, error_code: str | None = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

        super().__init__(self.detail)


class NotFoundError(AppException):
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(
            status_code=404,
            detail=detail,
            error_code="NOT_FOUND"
        )

class ForbiddenError(AppException):
    def __init__(self, detail: str = "Доступ запрещен"):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code="FORBIDDEN"
        )

class BadRequestError(AppException):
    def __init__(self, detail: str = "Некорректный запрос"):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="BAD_REQUEST"
        )

class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Пользователь не авторизован"):
        super().__init__(
            status_code=401,
            detail=detail,
            error_code="UNAUTHORIZED"
        )

class ConflictError(AppException):
    def __init__(self, detail: str = "Конфликт"):
        super().__init__(
            status_code=409,
            detail=detail,
            error_code="CONFLICT"
        )