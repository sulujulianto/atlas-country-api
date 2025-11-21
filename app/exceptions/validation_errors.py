class ValidationError(Exception):
    def __init__(self, message: str = "Validation failed", details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)
