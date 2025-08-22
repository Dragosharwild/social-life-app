class DomainError(Exception):
    pass


class DuplicateUser(DomainError):
    def __init__(self, field: str):
        super().__init__(f"That {field} is already taken.")
        self.field = field


class AuthFailed(DomainError):
    pass


class NotFound(DomainError):
    pass
