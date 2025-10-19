from flask import Flask, request, render_template, redirect, url_for, session, abort
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "secret"

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

USER = {"username": "alice", "password": "password123"}

comments = []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == USER['username'] and p == USER['password']:
            session.clear()
            session['user'] = u
            session['session_id'] = str(uuid4())
            return redirect(url_for('profile'))
        return "Bad request", 401
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        c = request.form.get('comment', '')
        comments.append(c)
    return render_template('profile_secure.html', user=session['user'], comments=comments)

if __name__ == "__main__":
    app.run(debug=True)