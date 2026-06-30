from fastapi import APIRouter
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter()
service = AuthService()

@router.post("/login")
def login(req: LoginRequest):
    token = service.login(req.username, req.password)
    return {"access_token": token}