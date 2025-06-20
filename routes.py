from flask import Flask, render_template, request, redirect, session, jsonify
from db import Database
from user_manager import UserManager
from access_manager import AccessManager

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"

    db = Database()
    user_manager = UserManager(db)
    access_manager = AccessManager(db)

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = user_manager.get_user(request.form["username"])
            if user and user[2] == request.form["password"]:
                session["user_id"] = user[0]
                return redirect("/dashboard")
            return "Неверный логин или пароль"
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            success, error = user_manager.create_user(request.form["username"], request.form["password"])
            if success:
                return redirect("/")
            else:
                return error
        return render_template("register.html")

    @app.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        if "user_id" not in session:
            return redirect("/")
        uid = session["user_id"]

        if request.method == "POST":
            action = request.form.get("action")

            if action == "toggle_access":
                program = request.form["program"]
                enabled = not access_manager.get_access(uid, program)
                flags = access_manager.get_flags(uid, program)
                access_manager.set_access_and_flags(uid, program, enabled, flags)
            
            elif action == "rename_program":
                program = request.form["program"]
                new_name = request.form["new_name"]
                access_manager.rename_program(uid, program, new_name)
            
            elif action == "delete_program":
                program = request.form["program"]
                access_manager.delete_program(uid, program)
            
            else:
                # обычное добавление новой программы
                program = request.form["program"]
                enabled = bool(request.form.get("enabled"))
                flags_dict = {flag: bool(request.form.get(flag)) for flag in access_manager.FLAGS}
                access_manager.set_access_and_flags(uid, program, enabled, flags_dict)
            

        user = user_manager.get_user_by_id(uid)
        programs = access_manager.get_programs(uid)

        program_flags = {}
        for program, _ in programs:
            program_flags[program] = access_manager.get_flags(uid, program)

        return render_template("dashboard.html",
                               username=user[1],
                               api_key=user[3],
                               programs=programs,
                               program_flags=program_flags)

    @app.route("/api/check_access", methods=["POST"])
    def check_access():
        data = request.json
        key = data.get("api_key")
        program = data.get("program")

        with db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM users WHERE api_key=?", (key,))
            row = cur.fetchone()
            if not row:
                return jsonify({"access": False, "error": "invalid api key"}), 403
            user = row[0]

        access = access_manager.get_access(user, program)
        return jsonify({"access": access})

    @app.route("/api/get_flags", methods=["POST"])
    def get_flags():
        data = request.json
        key = data.get("api_key")
        program = data.get("program")

        with db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM users WHERE api_key=?", (key,))
            row = cur.fetchone()
            if not row:
                return jsonify({"error": "Invalid API key"}), 403
            user = row[0]

        flags = access_manager.get_flags(user, program)
        return jsonify(flags)

    return app
