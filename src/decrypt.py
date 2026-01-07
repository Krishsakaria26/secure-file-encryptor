import argparse
import getpass
import hmac
import hashlib
import base64
from pathlib import Path
from tqdm import tqdm
from cryptography.fernet import Fernet, InvalidToken
from src.key_manager import derive_keys
from src.utils import read_file, write_file, decompress_data, find_files
from src.key_file_manager import load_key_file, validate_key_file
from src.logger import setup_logging
from src.config import get_config

def decrypt_file(file_path: str, output_path: str = None, password: str = None, 
                 keyfile: str = None, decompress: bool = False):
    """
    Decrypt a single file with optional decompression.
    """
    logger = setup_logging()
    config = get_config()
    
    try:
        data = read_file(file_path)
        
        if len(data) < 48:
            print(f"[-] File too small or corrupted: {file_path}")
            logger.error(f"File too small: {file_path}")
            return False

        salt = data[:16]
        stored_mac = data[16:48]
        ciphertext = data[48:]

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

        # Verify integrity
        computed_mac = hmac.new(hmac_key, ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(stored_mac, computed_mac):
            print(f"[-] Integrity check failed (wrong password or tampered file)")
            logger.error(f"Integrity check failed for {file_path}")
            return False

        # Decrypt
        cipher = Fernet(enc_key)
        try:
            plaintext = cipher.decrypt(ciphertext)
        except InvalidToken:
            print(f"[-] Decryption failed for {file_path}")
            logger.error(f"Decryption failed: {file_path}")
            return False

        # Decompress if needed
        if decompress:
            try:
                plaintext = decompress_data(plaintext)
                logger.info(f"Decompressed {file_path}")
            except Exception as e:
                print(f"[-] Decompression failed (file may not be compressed): {e}")
                logger.warning(f"Decompression failed for {file_path}: {e}")

        # Determine output path
        if not output_path:
            output_path = file_path.replace(".enc", "") if file_path.endswith(".enc") else file_path + ".dec"

        write_file(output_path, plaintext)
        print(f"[+] File decrypted: {output_path}")
        logger.info(f"Decrypted {file_path} -> {output_path}")
        
        return True

    except Exception as e:
        print(f"[-] Error decrypting {file_path}: {e}")
        logger.error(f"Error decrypting {file_path}: {e}")
        return False

def decrypt_batch(file_pattern: str, password: str = None, keyfile: str = None, decompress: bool = False):
    """
    Decrypt multiple files matching pattern.
    """
    files = find_files(file_pattern)
    
    if not files:
        print(f"[-] No files found matching: {file_pattern}")
        return
    
    print(f"[*] Found {len(files)} file(s) to decrypt")
    
    for file_path in tqdm(files, desc="Decrypting files"):
        decrypt_file(file_path, None, password, keyfile, decompress)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure File Decryptor")
    parser.add_argument("--file", required=True, help="Encrypted file or pattern")
    parser.add_argument("--out", help="Output file name")
    parser.add_argument("--password", help="Decryption password (will prompt if not provided)")
    parser.add_argument("--keyfile", help="Use key file instead of password")
    parser.add_argument("--decompress", action="store_true", help="Decompress after decryption")
    args = parser.parse_args()

    # Determine password or keyfile
    if args.keyfile:
        if not validate_key_file(args.keyfile):
            print(f"[-] Invalid key file: {args.keyfile}")
            exit(1)
        password = None
    else:
        password = args.password or getpass.getpass("Enter decryption password: ")
    
    # Check if pattern has wildcards or is directory
    if "*" in args.file or "?" in args.file or (Path(args.file).exists() and Path(args.file).is_dir()):
        decrypt_batch(args.file, password, args.keyfile, args.decompress)
    else:
        decrypt_file(args.file, args.out, password, args.keyfile, args.decompress)
