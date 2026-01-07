import argparse
import hmac
import hashlib
from src.utils import read_file

def verify_file(file_path: str, password: str = None):
    """
    Verify file integrity without full decryption.
    Checks the HMAC stored in the encrypted file.
    """
    try:
        data = read_file(file_path)
        
        if len(data) < 48:
            print(f"[-] File too small to verify (corrupted?)")
            return False
        
        salt = data[:16]
        stored_mac = data[16:48]
        
        if password:
            from src.key_manager import derive_keys
            _, hmac_key = derive_keys(password, salt)
            ciphertext = data[48:]
            computed_mac = hmac.new(hmac_key, ciphertext, hashlib.sha256).digest()
            
            if hmac.compare_digest(stored_mac, computed_mac):
                print(f"[+] File integrity verified - HMAC matches")
                return True
            else:
                print(f"[-] File integrity check FAILED - HMAC mismatch (wrong password or tampered)")
                return False
        else:
            print(f"[+] File has valid encrypted structure")
            return True
            
    except Exception as e:
        print(f"[-] Error verifying file: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify Encrypted File Integrity")
    parser.add_argument("--file", required=True, help="Encrypted file to verify")
    parser.add_argument("--password", help="Password for verification")
    args = parser.parse_args()
    
    import getpass
    password = args.password or (getpass.getpass("Enter password (optional): ") if args.password is None else None)
    verify_file(args.file, password)
