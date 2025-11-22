class ValidationError(Exception):
    code = "ERR_VALIDATION"
    status_code = 422

    def __init__(self, message: str = "Validation failed", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)
