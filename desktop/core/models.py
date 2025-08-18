from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: datetime


@dataclass(frozen=True)
class InnerCircle:
    id: int
    name: str
    interest: str
    description: str
    creator_id: int
    created_at: datetime


@dataclass(frozen=True)
class Membership:
    user_id: int
    circle_id: int
    role: str  # 'owner' or 'member'
    joined_at: datetime
