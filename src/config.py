import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".secure_file_encryptor" / "config.json"

DEFAULT_CONFIG = {
    "compress": False,
    "shred_original": False,
    "log_operations": True,
    "log_directory": "logs",
    "iterations": 200_000,
    "salt_length": 16,
}

def load_config():
    """Load configuration from file or return defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except Exception as e:
            print(f"[-] Error loading config: {e}")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config: dict):
    """Save configuration to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"[+] Config saved to {CONFIG_FILE}")

def get_config():
    """Get current configuration."""
    return load_config()
