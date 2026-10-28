"""Security helpers shared by future blueprints."""
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
def hash_password(password: str) -> str:
    if len(password) < 14: raise ValueError("Use at least 14 characters")
    return generate_password_hash(password)
def verify_password(stored_hash: str, password: str) -> bool:
    return check_password_hash(stored_hash, password)
def secure_token() -> str: return secrets.token_urlsafe(48)
