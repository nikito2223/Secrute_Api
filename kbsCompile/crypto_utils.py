from cryptography.fernet import Fernet

# Генерация ключа — делайте один раз и храните отдельно
# key = Fernet.generate_key()
key = b'HFje9E2E4_aQeRH0o7_gkSJovb2tK5It1tLYcCa_3X4='  # <-- замените своим ключом

fernet = Fernet(key)

def encrypt_data(data: bytes) -> bytes:
    return fernet.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    return fernet.decrypt(token)
