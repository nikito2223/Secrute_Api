import json
from crypto_utils import decrypt_data

def read_kbs_file(path="boot_key.kbs"):
    with open(path, "rb") as f:
        encrypted = f.read()
    decrypted = decrypt_data(encrypted)
    data = json.loads(decrypted)
    return data

if __name__ == "__main__":
    kbs_data = read_kbs_file()
    for program, config in kbs_data.items():
        Secrute = config.get("flags", {}).get("Secrute", False)
        print(f"{program}: {'Доступ разрешон!' if Secrute else 'Доступ запрещен!'}")
