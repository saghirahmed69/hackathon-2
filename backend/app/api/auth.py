"""
Authentication API routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas.auth import SignupRequest, SigninRequest, UserResponse, AuthResponse
from app.services.auth_service import signup, signin

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup_endpoint(
    data: SignupRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Create a new user account and return JWT token (auto-login).

    Args:
        data: Signup request with email and password
        session: Database session

    Returns:
        Auth response with JWT token and user data

    Raises:
        HTTPException 409: Email already registered
        HTTPException 400: Invalid request data
        HTTPException 500: Server error
    """
    try:
        user = await signup(session, data)
        return user
    except HTTPException:
        # Re-raise HTTP exceptions from service layer
        raise
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user account: {str(e)}",
        )


@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def signin_endpoint(
    data: SigninRequest,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """
    Authenticate user and return JWT token.

    Args:
        data: Signin request with email and password
        session: Database session

    Returns:
        Authentication response with JWT token and user data

    Raises:
        HTTPException 401: Invalid credentials
        HTTPException 400: Invalid request data
        HTTPException 500: Server error
    """
    try:
        auth_response = await signin(session, data)
        return auth_response
    except HTTPException:
        # Re-raise HTTP exceptions from service layer
        raise
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_endpoint() -> dict:
    """
    Logout endpoint (stateless - client discards token).

    Since JWT is stateless, logout is handled client-side by discarding the token.
    This endpoint exists for API completeness and future enhancements (e.g., token blacklist).

    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}
