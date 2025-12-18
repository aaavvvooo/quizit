from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

_pwd_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password must not be empty")

    return _pwd_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    if not password or not hashed_password:
        return False

    try:
        return _pwd_hasher.verify(hashed_password, password)
    except (VerifyMismatchError, InvalidHash):
        return False

def needs_rehash(hashed_password: str) -> bool:
    try:
        return _pwd_hasher.check_needs_rehash(hashed_password)
    except InvalidHash:
        return True
