import os
import re
import math
import gzip
import glob
from pathlib import Path

def generate_salt(length: int = 16) -> bytes:
    """
    Generate a random salt for key derivation.
    """
    return os.urandom(length)

def read_file(file_path: str) -> bytes:
    """
    Read the contents of a file as bytes.
    """
    with open(file_path, "rb") as f:
        return f.read()

def write_file(file_path: str, data: bytes) -> None:
    """
    Write bytes to a file.
    """
    with open(file_path, "wb") as f:
        f.write(data)

def compress_data(data: bytes) -> bytes:
    """Compress data using gzip."""
    return gzip.compress(data, compresslevel=9)

def decompress_data(data: bytes) -> bytes:
    """Decompress gzip data."""
    return gzip.decompress(data)

def shred_file(file_path: str, passes: int = 3) -> bool:
    """
    Securely delete a file by overwriting it with random data multiple times.
    """
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, "ba+") as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"[-] Error shredding file {file_path}: {e}")
        return False

def find_files(pattern: str) -> list[str]:
    """Find files matching glob pattern or directory path."""
    if os.path.isdir(pattern):
        # Recursively find all files in directory
        return [str(p) for p in Path(pattern).rglob("*") if p.is_file()]
    else:
        # Use glob pattern
        return glob.glob(pattern, recursive=True)

def estimate_entropy(password: str) -> float:
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)

def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 10:
        return False, "Password must be at least 10 characters long"

    rules = [
        (r"[a-z]", "lowercase letter"),
        (r"[A-Z]", "uppercase letter"),
        (r"[0-9]", "digit"),
        (r"[^a-zA-Z0-9]", "special character")
    ]

    for pattern, desc in rules:
        if not re.search(pattern, password):
            return False, f"Password must contain at least one {desc}"

    entropy = estimate_entropy(password)
    if entropy < 50:
        return False, f"Password entropy too low ({entropy:.1f} bits)"

    return True, f"Strong password (entropy: {entropy:.1f} bits)"
