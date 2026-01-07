import argparse
import getpass
import hmac
import hashlib
import base64
from pathlib import Path
from tqdm import tqdm
from cryptography.fernet import Fernet
from src.key_manager import derive_keys
from src.utils import (
    generate_salt, read_file, write_file, validate_password,
    compress_data, shred_file, find_files
)
from src.key_file_manager import load_key_file, validate_key_file
from src.logger import setup_logging
from src.config import get_config

def encrypt_file(file_path: str, password: str = None, keyfile: str = None, 
                 compress: bool = False, shred: bool = False, output: str = None):
    """
    Encrypt a single file with optional compression and file shredding.
    """
    logger = setup_logging()
    config = get_config()
    
    try:
        # Determine output path
        output_file = output or (file_path + ".enc")
        
        # Read file
        plaintext = read_file(file_path)
        
        # Compress if requested
        if compress:
            plaintext = compress_data(plaintext)
            logger.info(f"Compressed {file_path}")
        
        # Generate salt
        salt = generate_salt(config["salt_length"])
        
        # Derive keys
        if keyfile:
            if not validate_key_file(keyfile):
                print(f"[-] Invalid key file: {keyfile}")
                logger.error(f"Invalid key file: {keyfile}")
                return False
            key_material = load_key_file(keyfile)
            enc_key = base64.urlsafe_b64encode(key_material[:32])
            hmac_key = key_material[32:] if len(key_material) > 32 else b'\x00' * 32
        else:
            enc_key, hmac_key = derive_keys(password, salt)
        
        # Encrypt
        cipher = Fernet(enc_key)
        ciphertext = cipher.encrypt(plaintext)
        
        # Calculate HMAC
        mac = hmac.new(hmac_key, ciphertext, hashlib.sha256).digest()
        
        # Combine: salt + mac + ciphertext
        secure_blob = salt + mac + ciphertext
        
        # Write encrypted file
        write_file(output_file, secure_blob)
        print(f"[+] File encrypted: {output_file}")
        logger.info(f"Encrypted {file_path} -> {output_file}")
        
        # Shred original if requested
        if shred:
            if shred_file(file_path):
                print(f"[+] Original file securely deleted")
                logger.info(f"Shredded original file: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"[-] Error encrypting {file_path}: {e}")
        logger.error(f"Error encrypting {file_path}: {e}")
        return False

def encrypt_batch(file_pattern: str, password: str = None, keyfile: str = None,
                  compress: bool = False, shred: bool = False):
    """
    Encrypt multiple files matching pattern or in directory.
    """
    files = find_files(file_pattern)
    
    if not files:
        print(f"[-] No files found matching: {file_pattern}")
        return
    
    print(f"[*] Found {len(files)} file(s) to encrypt")
    
    for file_path in tqdm(files, desc="Encrypting files"):
        encrypt_file(file_path, password, keyfile, compress, shred)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure File Encryptor")
    parser.add_argument("--file", required=True, help="File or pattern to encrypt")
    parser.add_argument("--password", help="Encryption password (will prompt if not provided)")
    parser.add_argument("--keyfile", help="Use key file instead of password")
    parser.add_argument("--compress", action="store_true", help="Compress before encryption")
    parser.add_argument("--shred", action="store_true", help="Securely delete original file")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()
    
    # Determine password or keyfile
    if args.keyfile:
        if not validate_key_file(args.keyfile):
            print(f"[-] Invalid key file: {args.keyfile}")
            exit(1)
        password = None
    else:
        password = args.password or getpass.getpass("Enter encryption password: ")
        valid, message = validate_password(password)
        if not valid:
            print(f"[-] Weak password rejected: {message}")
            exit(1)
        print(f"[+] {message}")
    
    # Check if pattern has wildcards or is directory
    if "*" in args.file or "?" in args.file or (Path(args.file).exists() and Path(args.file).is_dir()):
        encrypt_batch(args.file, password, args.keyfile, args.compress, args.shred)
    else:
        encrypt_file(args.file, password, args.keyfile, args.compress, args.shred, args.output)
