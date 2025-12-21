"""
Pydantic schemas for authentication requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user signup."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class SigninRequest(BaseModel):
    """Request schema for user signin."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response schema for user data (no password)."""

    id: str
    email: str
    created_at: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for authentication (signin)."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
