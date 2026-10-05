from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt

from idp_common.config.settings import settings


class AuthService:

    def login(self, username: str, password: str) -> str:

        if (
            username != settings.API_USERNAME
            or password != settings.API_PASSWORD
        ):
            raise ValueError("Invalid credentials")

        payload = {
            "sub": username,
            "exp": datetime.now(timezone.utc)
            + timedelta(hours=settings.JWT_EXPIRE_HOURS),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    def verify_token(self, token: str) -> dict:

        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
