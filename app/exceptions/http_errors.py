class BadRequestError(Exception):
    def __init__(self, message: str = "Bad request", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str = "Resource not found", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)
