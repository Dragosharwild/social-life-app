from typing import Iterable

from core.models import InnerCircle
from core.ports import CircleRepository


class CircleService:
	def __init__(self, repo: CircleRepository):
		self.repo = repo

	def create(self, name: str, interest: str, description: str, creator_id: int) -> InnerCircle:
		circle = self.repo.create_circle(name, interest, description, creator_id)
		# ensure owner membership (repo already inserts with IGNORE)
		self.repo.add_membership(creator_id, circle.id, role="owner")
		return circle

	def search(self, query: str) -> Iterable[InnerCircle]:
		return self.repo.search(query)

	def join(self, user_id: int, circle_id: int) -> None:
		self.repo.join(user_id, circle_id)

	def leave(self, user_id: int, circle_id: int) -> None:
		self.repo.leave(user_id, circle_id)

	def details(self, circle_id: int):
		return self.repo.get_details(circle_id)

	def user_has_any_memberships(self, user_id: int) -> bool:
		return self.repo.has_memberships(user_id)

