import hashlib
import hmac
import os


def hash_password(password: str, salt: bytes | None = None) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a random salt.

    Args:
        password: The plaintext password to hash.
        salt: Optional salt bytes. If not provided, a random 16-byte salt is generated.

    Returns:
        A string in the format 'salt$hash' where both parts are hex-encoded.
    """
    if salt is None:
        salt = os.urandom(16)

    # PBKDF2 with HMAC-SHA256, 100_000 iterations, 32-byte derived key
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100_000,
        dklen=32
    )

    return f"{salt.hex()}${dk.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a plaintext password against a stored hash.

    Args:
        password: The plaintext password to check.
        stored_hash: The stored hash string in 'salt$hash' format.

    Returns:
        True if the password matches, False otherwise.
    """
    try:
        salt_hex, hash_hex = stored_hash.split('$', 1)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False

    computed = hash_password(password, salt)
    # Use compare_digest to prevent timing attacks
    return hmac.compare_digest(computed, stored_hash)
