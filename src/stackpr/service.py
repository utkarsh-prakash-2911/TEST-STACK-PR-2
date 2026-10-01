"""User service layer.

Business logic built on top of the :class:`~stackpr.user.User` domain model
introduced in PR #1. Provides create/get operations backed by an in-memory
store.
"""

from __future__ import annotations

from uuid import UUID

from .user import User, UserRole


class UserAlreadyExistsError(Exception):
    """Raised when creating a user whose email is already registered."""


class UserNotFoundError(Exception):
    """Raised when a requested user cannot be found."""


class UserService:
    """Service exposing business operations over the ``User`` domain.

    Users are held in a simple in-memory store keyed by their id, with an
    email index to enforce uniqueness.
    """

    def __init__(self) -> None:
        self._by_id: dict[UUID, User] = {}
        self._by_email: dict[str, UUID] = {}

    def create_user(
        self, email: str, name: str, role: UserRole = UserRole.MEMBER
    ) -> User:
        """Create and store a new user.

        Raises:
            UserAlreadyExistsError: If ``email`` is already registered.
        """
        key = email.lower()
        if key in self._by_email:
            raise UserAlreadyExistsError(email)

        user = User(email=email, name=name, role=role)
        self._by_id[user.id] = user
        self._by_email[key] = user.id
        return user

    def get_user(self, user_id: UUID) -> User:
        """Return the user with ``user_id``.

        Raises:
            UserNotFoundError: If no such user exists.
        """
        try:
            return self._by_id[user_id]
        except KeyError:
            raise UserNotFoundError(str(user_id)) from None

    def get_user_by_email(self, email: str) -> User:
        """Return the user registered with ``email``.

        Raises:
            UserNotFoundError: If no such user exists.
        """
        user_id = self._by_email.get(email.lower())
        if user_id is None:
            raise UserNotFoundError(email)
        return self._by_id[user_id]

    def list_users(self) -> list[User]:
        """Return all stored users."""
        return list(self._by_id.values())
