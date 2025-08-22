from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .models import User, InnerCircle


class AuthRepository(ABC):
	@abstractmethod
	def create_user(self, email: str, username: str, password_hash: str) -> User:  # may raise Duplicate
		raise NotImplementedError

	@abstractmethod
	def get_user_by_identity(self, identifier: str) -> Optional[User]:
		"""Look up by username or email (case-insensitive)."""
		raise NotImplementedError


class CircleRepository(ABC):
	@abstractmethod
	def create_circle(self, name: str, interest: str, description: str, creator_id: int) -> InnerCircle:
		raise NotImplementedError

	@abstractmethod
	def add_membership(self, user_id: int, circle_id: int, role: str) -> None:
		raise NotImplementedError

	@abstractmethod
	def search(self, query: str) -> Iterable[InnerCircle]:
		raise NotImplementedError

	@abstractmethod
	def get_details(self, circle_id: int) -> tuple[InnerCircle, int, User]:
		"""Return (circle, member_count, creator)."""
		raise NotImplementedError

	@abstractmethod
	def join(self, user_id: int, circle_id: int) -> None:
		raise NotImplementedError

	@abstractmethod
	def leave(self, user_id: int, circle_id: int) -> None:
		raise NotImplementedError

	@abstractmethod
	def has_memberships(self, user_id: int) -> bool:
		"""Return True if user belongs to any circle (owner or member)."""
		raise NotImplementedError

