# Secure File Encryptor

A robust, feature-rich file encryption tool with support for batch operations, compression, secure file shredding, and integrity verification.

## Features

- **AES-256 Encryption** - Uses Fernet (symmetric encryption) with PBKDF2 key derivation
- **HMAC Authentication** - Verifies file integrity and authenticity
- **Password-based & Key File Support** - Encrypt with passwords or key files
- **Batch Operations** - Encrypt/decrypt multiple files or entire directories
- **Compression** - Optional gzip compression before encryption
- **Secure File Shredding** - Safely delete original files with multiple passes
- **Progress Tracking** - Visual progress bar for batch operations
- **File Integrity Verification** - Verify encrypted files without decryption
- **Logging** - Comprehensive operation logging
- **Configuration** - Customizable settings via config file

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone or download the project
cd secure-file-encryptor

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Encrypt a File

#### Using Password:
```bash
python -m src.encrypt --file test.txt
Enter encryption password: Krish12345
[+] Strong password (entropy: 91.8 bits)
[+] File encrypted: test.txt.enc
```

#### With Compression:
```bash
python -m src.encrypt --file test.txt --compress
```

#### With Secure Deletion:
```bash
python -m src.encrypt --file test.txt --shred
```

#### Using Key File:
```bash
# First, generate a key file
python -c "from src.key_file_manager import generate_key_file; generate_key_file('.key')"

# Then encrypt
python -m src.encrypt --file test.txt --keyfile .key
```

### Decrypt a File

#### Basic Decryption:
```bash
python -m src.decrypt --file test.txt.enc --out test.txt
Enter decryption password: Krish12345
[+] File decrypted: test.txt
```

#### With Decompression:
```bash
python -m src.decrypt --file test.txt.enc --out test.txt --decompress
```

#### Using Key File:
```bash
python -m src.decrypt --file test.txt.enc --out test.txt --keyfile .key
```

### Batch Operations

#### Encrypt All Files in Directory:
```bash
python -m src.encrypt --file ./documents/
```

#### Encrypt with Pattern:
```bash
python -m src.encrypt --file "*.txt"
```

#### Decrypt All .enc Files:
```bash
python -m src.decrypt --file "*.enc"
```

### Verify File Integrity

```bash
python -m src.verify --file test.txt.enc --password Krish12345
[+] File integrity verified - HMAC matches
```

Or without password:
```bash
python -m src.verify --file test.txt.enc
[+] File has valid encrypted structure
```

## Password Requirements

Passwords must meet the following criteria:
- Minimum 10 characters
- At least one lowercase letter
- At least one uppercase letter
- At least one digit
- At least one special character
- Minimum entropy of 50 bits

Example strong password: `MyPass123!@`

## Configuration

Configuration is stored at `~/.secure_file_encryptor/config.json`

Default settings:
```json
{
  "compress": false,
  "shred_original": false,
  "log_operations": true,
  "log_directory": "logs",
  "iterations": 200000,
  "salt_length": 16
}
```

## File Format

Encrypted files have the following structure:
```
[Salt (16 bytes)] + [HMAC-SHA256 (32 bytes)] + [Encrypted Data]
```

## Security Notes

- **Key Derivation**: PBKDF2-HMAC-SHA256 with 200,000 iterations
- **Encryption**: Fernet (AES-128 in CBC mode with HMAC authentication)
- **File Shredding**: 3-pass overwrite with random data before deletion
- **HMAC**: Verifies both authenticity and integrity

## Examples

### Encrypt Important Documents
```bash
python -m src.encrypt --file ~/Documents/sensitive/ --compress --shred
```

### Backup with Encryption
```bash
python -m src.encrypt --file backup.tar.gz --compress --output backup.secure
```

### Encrypt Logs (Batch)
```bash
python -m src.encrypt --file "*.log" --shred
```

## Logging

All operations are logged to `logs/encryptor_YYYYMMDD_HHMMSS.log`

Check logs for:
- File encryption/decryption events
- Errors and warnings
- Compression and shredding operations

## Troubleshooting

### "Weak password rejected"
- Ensure password meets all requirements
- Use at least one uppercase letter, number, and special character

### "Integrity check failed"
- Wrong password provided
- File may be corrupted
- File may have been tampered with

### "File too small or corrupted"
- File may not be a valid encrypted file
- File may be corrupted during transfer

## License

MIT License - See LICENSE file for details

## Contributing

Feel free to submit issues and enhancement requests!
