"""
Authentication service with password hashing and JWT token generation.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional

from app.models.user import User
from app.schemas.auth import SignupRequest, SigninRequest, UserResponse, AuthResponse
from app.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: User ID to encode in token

    Returns:
        JWT token string
    """
    expires = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "exp": expires,
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def signup(session: AsyncSession, data: SignupRequest) -> AuthResponse:
    """
    Create a new user account and return JWT token (auto-login).

    Args:
        session: Database session
        data: Signup request data

    Returns:
        Auth response with JWT token and user data

    Raises:
        HTTPException 409: If email already registered
    """
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Create access token (auto-login after signup)
    access_token = create_access_token(user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at.isoformat(),
        ),
    )


async def signin(session: AsyncSession, data: SigninRequest) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    Args:
        session: Database session
        data: Signin request data

    Returns:
        Auth response with JWT token and user data

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Get user by email
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create access token
    access_token = create_access_token(user.id)

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at.isoformat(),
        ),
    )
