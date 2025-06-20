import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Путь к корневой директории проекта (относительно /kbsCompile)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Загружаем .env
load_dotenv(dotenv_path=ENV_PATH)

# Получаем ключ
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY не найден в .env")

# Инициализируем шифратор
cipher = Fernet(FERNET_KEY)


# ✅ Функции шифрования / дешифрования
def encrypt_data(data: str) -> bytes:
    return cipher.encrypt(data.encode())


def decrypt_data(data: bytes) -> str:
    return cipher.decrypt(data).decode()
