import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# создаем базу данных и таблицу пользователей
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT
                )""")
    # добавляем тестового пользователя
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "12345"))
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ❌ УЯЗВИМЫЙ SQL ЗАПРОС (строка форматирования!)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return redirect(url_for("dashboard", user=username))
        else:
            message = "Неверный логин или пароль!"
    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    user = request.args.get("user")
    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
