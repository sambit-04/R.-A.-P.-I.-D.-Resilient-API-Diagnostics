from cryptography.fernet import Fernet
import os

KEY_PATH = os.path.join(os.path.dirname(__file__), ".fernet.key")

def ensure_key():
    if os.path.exists(KEY_PATH):
        return open(KEY_PATH, "rb").read()
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f: f.write(key)
    return key

KEY = ensure_key()
cipher = Fernet(KEY)

def encrypt_data(plain: str) -> str:
    return cipher.encrypt(plain.encode()).decode()

def decrypt_data(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
