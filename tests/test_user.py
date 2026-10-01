import pytest

from stackpr.user import User, UserRole


def test_user_defaults():
    user = User(email="alice@example.com", name="Alice")
    assert user.role is UserRole.MEMBER
    assert user.is_active is True
    assert user.is_admin is False
    assert user.id is not None


def test_admin_role():
    user = User(email="root@example.com", name="Root", role=UserRole.ADMIN)
    assert user.is_admin is True


def test_deactivate():
    user = User(email="bob@example.com", name="Bob")
    user.deactivate()
    assert user.is_active is False


def test_invalid_email():
    with pytest.raises(ValueError):
        User(email="not-an-email", name="Nobody")


def test_empty_name():
    with pytest.raises(ValueError):
        User(email="x@example.com", name="   ")
