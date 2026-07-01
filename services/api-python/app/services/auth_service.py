class AuthService:
    def login(self, username: str, password: str) -> str:
        if username == "admin" and password == "admin":
            return "fake-jwt-token"
        raise Exception("Invalid credentials")