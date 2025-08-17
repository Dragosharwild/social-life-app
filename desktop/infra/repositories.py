from __future__ import annotations

import sqlite3
from typing import Iterable, Optional

from core.errors import DuplicateUser, NotFound
from core.models import InnerCircle, User
from core.ports import AuthRepository, CircleRepository
from .db import get_connection


class SQLiteAuthRepository(AuthRepository):
	def create_user(self, email: str, username: str, password_hash: str) -> User:
		with get_connection() as conn:
			try:
				cur = conn.execute(
					"""
					INSERT INTO users (username, email, password_hash)
					VALUES (?, ?, ?)
					""",
					(username.strip(), email.strip(), password_hash),
				)
			except sqlite3.IntegrityError as e:
				msg = str(e).lower()
				if "username" in msg:
					raise DuplicateUser("username")
				if "email" in msg:
					raise DuplicateUser("email")
				raise

			rowid = cur.lastrowid
			row = conn.execute(
				"SELECT id, username, email, password_hash, created_at FROM users WHERE id=?",
				(rowid,),
			).fetchone()
			return User(
				id=row["id"],
				username=row["username"],
				email=row["email"],
				password_hash=row["password_hash"],
				created_at=row["created_at"],
			)

	def get_user_by_identity(self, identifier: str) -> Optional[User]:
		ident = identifier.strip()
		with get_connection() as conn:
			row = conn.execute(
				"""
				SELECT id, username, email, password_hash, created_at
				FROM users
				WHERE lower(username)=lower(?) OR lower(email)=lower(?)
				LIMIT 1
				""",
				(ident, ident),
			).fetchone()
			if not row:
				return None
			return User(
				id=row["id"],
				username=row["username"],
				email=row["email"],
				password_hash=row["password_hash"],
				created_at=row["created_at"],
			)


class SQLiteCircleRepository(CircleRepository):
	def create_circle(self, name: str, interest: str, description: str, creator_id: int) -> InnerCircle:
		with get_connection() as conn:
			cur = conn.execute(
				"""
				INSERT INTO circles (name, interest, description, creator_id)
				VALUES (?, ?, ?, ?)
				""",
				(name.strip(), interest.strip(), description.strip(), creator_id),
			)
			circle_id = cur.lastrowid
			# creator becomes owner
			conn.execute(
				"INSERT OR IGNORE INTO memberships (user_id, circle_id, role) VALUES (?, ?, 'owner')",
				(creator_id, circle_id),
			)
			row = conn.execute(
				"SELECT id, name, interest, description, creator_id, created_at FROM circles WHERE id=?",
				(circle_id,),
			).fetchone()
			return InnerCircle(
				id=row["id"],
				name=row["name"],
				interest=row["interest"],
				description=row["description"],
				creator_id=row["creator_id"],
				created_at=row["created_at"],
			)

	def add_membership(self, user_id: int, circle_id: int, role: str) -> None:
		with get_connection() as conn:
			conn.execute(
				"INSERT OR IGNORE INTO memberships (user_id, circle_id, role) VALUES (?, ?, ?)",
				(user_id, circle_id, role),
			)

	def search(self, query: str) -> Iterable[InnerCircle]:
		q = f"%{query.strip()}%"
		with get_connection() as conn:
			rows = conn.execute(
				"""
				SELECT id, name, interest, description, creator_id, created_at
				FROM circles
				WHERE name LIKE ? OR interest LIKE ?
				ORDER BY created_at DESC
				""",
				(q, q),
			).fetchall()
			for row in rows:
				yield InnerCircle(
					id=row["id"],
					name=row["name"],
					interest=row["interest"],
					description=row["description"],
					creator_id=row["creator_id"],
					created_at=row["created_at"],
				)

	def get_details(self, circle_id: int) -> tuple[InnerCircle, int, User]:
		with get_connection() as conn:
			c_row = conn.execute(
				"SELECT id, name, interest, description, creator_id, created_at FROM circles WHERE id=?",
				(circle_id,),
			).fetchone()
			if not c_row:
				raise NotFound("circle")
			count = conn.execute(
				"SELECT COUNT(*) FROM memberships WHERE circle_id=?",
				(circle_id,),
			).fetchone()[0]
			u_row = conn.execute(
				"SELECT id, username, email, password_hash, created_at FROM users WHERE id=?",
				(c_row["creator_id"],),
			).fetchone()
			circle = InnerCircle(
				id=c_row["id"],
				name=c_row["name"],
				interest=c_row["interest"],
				description=c_row["description"],
				creator_id=c_row["creator_id"],
				created_at=c_row["created_at"],
			)
			creator = User(
				id=u_row["id"],
				username=u_row["username"],
				email=u_row["email"],
				password_hash=u_row["password_hash"],
				created_at=u_row["created_at"],
			)
			return circle, int(count), creator

	def join(self, user_id: int, circle_id: int) -> None:
		with get_connection() as conn:
			conn.execute(
				"INSERT OR IGNORE INTO memberships (user_id, circle_id, role) VALUES (?, ?, 'member')",
				(user_id, circle_id),
			)

	def leave(self, user_id: int, circle_id: int) -> None:
		with get_connection() as conn:
			conn.execute(
				"DELETE FROM memberships WHERE user_id=? AND circle_id=?",
				(user_id, circle_id),
			)

	def has_memberships(self, user_id: int) -> bool:
		with get_connection() as conn:
			row = conn.execute(
				"SELECT 1 FROM memberships WHERE user_id=? LIMIT 1",
				(user_id,),
			).fetchone()
		return bool(row)

