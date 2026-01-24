"""Security helpers: password hashing and verification.

Provides a small abstraction over werkzeug security functions so the
application code depends on a single, testable API.
"""
from typing import Any

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """Return a secure hash for the given password.

    Args:
        password: plaintext password

    Returns:
        A string containing the hashed password.
    """
    return generate_password_hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a plaintext password against the stored hash.

    Args:
        stored_hash: hash retrieved from storage
        password: plaintext password to verify

    Returns:
        True if the password matches the hash, False otherwise.
    """
    # type: (str, str) -> bool
    return check_password_hash(stored_hash, password)
