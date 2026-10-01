import pytest

from stackpr.service import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserService,
)
from stackpr.user import UserRole


def test_create_and_get_user():
    service = UserService()
    user = service.create_user("alice@example.com", "Alice")
    assert service.get_user(user.id) is user
    assert service.get_user_by_email("alice@example.com") is user


def test_create_user_role():
    service = UserService()
    user = service.create_user("root@example.com", "Root", role=UserRole.ADMIN)
    assert user.is_admin is True


def test_duplicate_email_rejected():
    service = UserService()
    service.create_user("dup@example.com", "First")
    with pytest.raises(UserAlreadyExistsError):
        service.create_user("DUP@example.com", "Second")


def test_get_missing_user_raises():
    service = UserService()
    with pytest.raises(UserNotFoundError):
        service.get_user_by_email("ghost@example.com")


def test_list_users():
    service = UserService()
    service.create_user("a@example.com", "A")
    service.create_user("b@example.com", "B")
    assert len(service.list_users()) == 2
