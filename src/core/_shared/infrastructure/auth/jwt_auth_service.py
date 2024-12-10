import os
from core._shared.infrastructure.auth.auth_interface import AuthServiceInterface
import jwt
import base64
from dotenv import load_dotenv

load_dotenv()

class JWTAuthService(AuthServiceInterface):
    def __init__(self, token: str = ""):
        self.public_key = os.getenv("AUTH_PUBLIC_KEY")
        self.token = token.replace("Bearer ", "", 1)

    def _decode_token(self) -> dict:
        try:
            return jwt.decode(self.token, self.public_key, algorithms=["RS256"], audience="account")
        except jwt.PyJWTError:
            return {}
        
    def is_authenticated(self) -> bool:
        return bool(self._decode_token())

    def has_role(self, role: str) -> bool:
        decoded_token = self._decode_token()
        return role in decoded_token.get('realm_access', {}).get('roles', [])