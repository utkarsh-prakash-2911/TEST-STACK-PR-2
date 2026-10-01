"""User domain model.

This module defines the core ``User`` entity along with the supporting
types used across the service and API layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """Roles a user can hold within the system."""

    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


@dataclass
class User:
    """Core user entity.

    Attributes:
        email: The user's email address; serves as the login identifier.
        name: The user's display name.
        role: The user's role. Defaults to :attr:`UserRole.MEMBER`.
        id: Stable unique identifier, generated if not supplied.
        created_at: UTC timestamp of when the user was created.
        is_active: Whether the account is currently active.
    """

    email: str
    name: str
    role: UserRole = UserRole.MEMBER
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    is_active: bool = True

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError(f"invalid email address: {self.email!r}")
        if not self.name.strip():
            raise ValueError("name must not be empty")

    @property
    def is_admin(self) -> bool:
        """Return ``True`` if the user holds the admin role."""
        return self.role is UserRole.ADMIN

    def deactivate(self) -> None:
        """Mark the user account as inactive."""
        self.is_active = False
