import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def derive_keys(password: str, salt: bytes) -> tuple[bytes, bytes]:
    """
    Derive separate keys for encryption and HMAC using PBKDF2.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=64,   
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )

    key_material = kdf.derive(password.encode())
    enc_key = base64.urlsafe_b64encode(key_material[:32])
    hmac_key = key_material[32:]

    return enc_key, hmac_key
