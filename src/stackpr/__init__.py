"""stackpr: a tiny package used to demonstrate Stacked PR workflows."""

from .core import add, greet
from .service import UserAlreadyExistsError, UserNotFoundError, UserService
from .user import User, UserRole

__all__ = [
    "add",
    "greet",
    "User",
    "UserRole",
    "UserService",
    "UserAlreadyExistsError",
    "UserNotFoundError",
    "create_app",
]


def create_app():
    """Lazily build the FastAPI app (keeps web deps optional at import time)."""
    from .api import create_app as _create_app

    return _create_app()
__version__ = "0.1.0"
