import secrets
import string

class CodeGenerator:
    """Generates unique short codes for URLs.
    Currently uses cryptographically secure random choices from alphanumeric characters (Base62 set)."""
    # Alphabet contains 62 characters: A-Z, a-z, 0-9
    ALPHABET = string.ascii_letters + string.digits
    DEFAULT_LENGTH = 6

    @classmethod
    def generate(cls, length: int = DEFAULT_LENGTH) -> str:
        """Generates a random string of a specified length using cryptographically secure random selection"""
        return "".join(secrets.choice(cls.ALPHABET) for _ in range(length))
