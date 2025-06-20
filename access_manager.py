class AccessManager:
    FLAGS = ["io_secrute", "file_system", "net_control", "Secrute"]

    def __init__(self, db):
        self.db = db

    def get_access(self, user_id, program):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT enabled FROM access WHERE user_id=? AND program_name=?", (user_id, program))
            row = cur.fetchone()
            return row[0] == 1 if row else False

    def set_access_and_flags(self, user_id, program, enabled, flags_dict):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM access WHERE user_id=? AND program_name=?", (user_id, program))
            if cur.fetchone():
                cur.execute("UPDATE access SET enabled=? WHERE user_id=? AND program_name=?",
                            (1 if enabled else 0, user_id, program))
            else:
                cur.execute("INSERT INTO access (user_id, program_name, enabled) VALUES (?, ?, ?)",
                            (user_id, program, 1 if enabled else 0))

            for flag in self.FLAGS:
                cur.execute("""
                    INSERT OR REPLACE INTO flags (user_id, program_name, flag_name, flag_value)
                    VALUES (?, ?, ?, ?)
                """, (user_id, program, flag, 1 if flags_dict.get(flag) else 0))

            con.commit()

    def get_programs(self, user_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT program_name, enabled FROM access WHERE user_id=?", (user_id,))
            return cur.fetchall()

    def get_flags(self, user_id, program):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT flag_name, flag_value FROM flags WHERE user_id=? AND program_name=?", (user_id, program))
            flags = {name: bool(val) for name, val in cur.fetchall()}
            flags["x_secrute"] = True  # всегда по умолчанию
            return flags
    def delete_program(self, user_id, program):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM access WHERE user_id=? AND program_name=?", (user_id, program))
            cur.execute("DELETE FROM flags WHERE user_id=? AND program_name=?", (user_id, program))
            con.commit()

    def rename_program(self, user_id, old_name, new_name):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("UPDATE access SET program_name=? WHERE user_id=? AND program_name=?", (new_name, user_id, old_name))
            cur.execute("UPDATE flags SET program_name=? WHERE user_id=? AND program_name=?", (new_name, user_id, old_name))
            con.commit()
