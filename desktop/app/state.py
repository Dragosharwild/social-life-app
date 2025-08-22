from dataclasses import dataclass
from typing import Optional

from core.models import User


@dataclass
class AppState:
    current_user: Optional[User] = None
    selected_circle_id: Optional[int] = None
