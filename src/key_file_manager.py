import os
from pathlib import Path

def generate_key_file(file_path: str) -> bytes:
    """Generate a random key file (256-bit key)."""
    key = os.urandom(32)
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(key)
    return key

def load_key_file(file_path: str) -> bytes:
    """Load key from file."""
    with open(file_path, "rb") as f:
        return f.read()

def validate_key_file(file_path: str) -> bool:
    """Check if key file exists and is valid."""
    return os.path.exists(file_path) and os.path.getsize(file_path) == 32
