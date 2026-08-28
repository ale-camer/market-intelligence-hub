"""Authentication router for issuing JWT access tokens."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token", response_model=dict[str, Any])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict[str, Any]:
    """Authenticate user and return JWT bearer access token."""
    # Standard dummy credential check for data serving API demonstration
    if form_data.username != "admin" or form_data.password != "admin":  # noqa: S105
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
