class BadRequestError(Exception):
    code = "ERR_BAD_REQUEST"
    status_code = 400

    def __init__(self, message: str = "Bad request", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(Exception):
    code = "ERR_NOT_FOUND"
    status_code = 404

    def __init__(self, message: str = "Resource not found", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)
