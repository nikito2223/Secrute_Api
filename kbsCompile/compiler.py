import sqlite3, json
from crypto_utils import encrypt_data

def compile_kbs(api_key):
    with sqlite3.connect("..\\db.sqlite3") as con:
        cur = con.cursor()
        cur.execute("SELECT id FROM users WHERE api_key=?", (api_key,))
        row = cur.fetchone()
        if not row:
            print("Пользователь не найден")
            return
        uid = row[0]

        cur.execute("SELECT program_name, enabled FROM access WHERE user_id=?", (uid,))
        access_list = cur.fetchall()

        result = {}
        for program, enabled in access_list:
            cur.execute("SELECT flag_name, flag_value FROM flags WHERE user_id=? AND program_name=?", (uid, program))
            flags = cur.fetchall()
            result[program] = {
                "enabled": bool(enabled),
                "flags": {name: bool(val) for name, val in flags}
            }
            result[program]["flags"]["x_secrute"] = True  # всегда по умолчанию

        encrypted = encrypt_data(json.dumps(result))  # encode() убран

        with open("boot_key.kbs", "wb") as f:
            f.write(encrypted)
        print("Файл boot_key.kbs создан.")

if __name__ == "__main__":
    compile_kbs("YOUR-API-USERS")
