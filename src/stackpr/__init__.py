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
]
__version__ = "0.1.0"
