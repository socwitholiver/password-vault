# main.py

from cryptography.fernet import Fernet
import os
from datetime import datetime

KEY_FILE = 'key.key'
VAULT_FILE = 'vault.txt'
MASTER_FILE = 'master.key'
LOG_FILE = 'activity.log'

# 🔐 Generate encryption key if missing
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

# 🔑 Load key (auto-generate if missing)
def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

# 🔒 Encrypt password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

# 🔓 Decrypt password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()

# ➕ Add a password
def add_password(site, password):
    encrypted = encrypt_password(password)
    with open(VAULT_FILE, 'a') as file:
        file.write(f"{site}|{encrypted}\n")
    log_event(f"Added password for {site}")

# 👁 Retrieve all passwords
def get_passwords():
    passwords = []
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as file:
            for line in file:
                if '|' in line:
                    site, enc = line.strip().split('|', 1)
                    try:
                        dec = decrypt_password(enc)
                        passwords.append((site, dec))
                    except:
                        passwords.append((site, 'DECRYPTION ERROR'))
    return passwords

# 🗑 Delete a site entry
def delete_password(site_name):
    if not os.path.exists(VAULT_FILE):
        return
    lines = []
    with open(VAULT_FILE, 'r') as file:
        lines = file.readlines()
    with open(VAULT_FILE, 'w') as file:
        for line in lines:
            if not line.startswith(site_name + "|"):
                file.write(line)
    log_event(f"Deleted password for {site_name}")

# 🔐 Save encrypted master password
def set_master_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    with open(MASTER_FILE, 'wb') as f:
        f.write(encrypted)
    log_event("Master password set")

# 🔐 Verify entered master password
def verify_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False
    key = load_key()
    fernet = Fernet(key)
    try:
        with open(MASTER_FILE, 'rb') as f:
            encrypted = f.read()
        valid = fernet.decrypt(encrypted).decode() == password
        log_event("Login success" if valid else "Login failed")
        return valid
    except:
        log_event("Login failed (exception)")
        return False

# 📜 Logging
def log_event(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
# trigger auto build
