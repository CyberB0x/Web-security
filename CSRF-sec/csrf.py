from flask import Flask, request, render_template, redirect, url_for, session, abort
import secrets

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Простая "база данных" пользователя
USER = {"username": "admin", "password": "12345"}

@app.route("/", methods=["GET", "POST"])
def index():
   if "csrf_token" not in session:
       session["csrf_token"] = secrets.token_hex(16)

   if request.method == "POST":
       form_token = request.form.get("csrf_token")

       if not form_token or form_token != session["csrf_token"]:
           abort(403)
       new_password = request.form.get("password")
       USER["password"] = new_password
       return redirect(url_for("success"))

   return render_template("index.html", user=USER, csrf_token=session["csrf_token"])


@app.route("/success")
def success():
    return render_template("success.html", user=USER)

if __name__ == "__main__":
    app.run(debug=True)
