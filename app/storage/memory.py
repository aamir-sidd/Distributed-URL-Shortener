import threading
from typing import Dict, Optional

class InMemoryStorage:
    """A thread-safe, in-memory repository using a Python dictionary and a threading lock. This serves as temporary datastore"""
    def __init__(self):
        # Map: short_code (str) -> original_url (str)
        self._db: Dict[str, str] = {}
        self._lock = threading.Lock()

    def save_url(self, short_code: str, original_url: str) -> None:
        """Saves a short code mapped to its original long URL."""
        with self._lock:
            self._db[short_code] = original_url

    def get_url(self, short_code: str) -> Optional[str]:
        """Retrieves the original URL for a given short code. Returns None if not found."""
        with self._lock:
            return self._db.get(short_code)

    def code_exists(self, short_code: str) -> bool:
        """Checks if a short code is already in use."""
        with self._lock:
            return short_code in self._db

# Instantiate a single global singleton instance of storage
storage = InMemoryStorage()
