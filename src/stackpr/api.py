"""User REST API.

Exposes the :class:`~stackpr.service.UserService` (introduced in PR #2)
through REST endpoints using FastAPI.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr

from .service import UserAlreadyExistsError, UserNotFoundError, UserService
from .user import UserRole


class CreateUserRequest(BaseModel):
    """Request body for creating a user."""

    email: EmailStr
    name: str
    role: UserRole = UserRole.MEMBER


class UserResponse(BaseModel):
    """API representation of a user."""

    id: UUID
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime


# A single service instance backs the app for this demo.
_service = UserService()


def get_service() -> UserService:
    """Dependency returning the shared :class:`UserService`."""
    return _service


def create_app() -> FastAPI:
    """Build and return the FastAPI application."""
    app = FastAPI(title="stackpr User API")

    @app.post(
        "/users",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_user(
        payload: CreateUserRequest,
        service: UserService = Depends(get_service),
    ) -> UserResponse:
        try:
            user = service.create_user(
                email=payload.email, name=payload.name, role=payload.role
            )
        except UserAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="a user with this email already exists",
            )
        return UserResponse(**vars(user))

    @app.get("/users/{user_id}", response_model=UserResponse)
    def get_user(
        user_id: UUID,
        service: UserService = Depends(get_service),
    ) -> UserResponse:
        try:
            user = service.get_user(user_id)
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found",
            )
        return UserResponse(**vars(user))

    return app


app = create_app()
