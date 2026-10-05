from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService


router = APIRouter()
service = AuthService()


@router.post("/login")
def login(req: LoginRequest):

    try:
        token = service.login(req.username, req.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    return {
        "access_token": token,
        "token_type": "bearer",
    }
