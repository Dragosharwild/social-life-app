from core.errors import AuthFailed, DuplicateUser
from core.ports import AuthRepository
from infra.security import hash_password, verify_password


class AuthService:
    """Sign up and login logic.

    Mirrors legacy behavior but uses hashed passwords and repository ports.
    """

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def sign_up(self, email: str, username: str, password: str):
        try:
            return self.repo.create_user(
                email=email,
                username=username,
                password_hash=hash_password(password),
            )
        except DuplicateUser:
            # propagate as-is; UI can present message
            raise

    def login(self, identifier: str, password: str):
        user = self.repo.get_user_by_identity(identifier)
        if not user or not verify_password(password, user.password_hash):
            raise AuthFailed("Invalid username/email or password.")
        return user
