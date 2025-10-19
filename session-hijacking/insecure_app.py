# insecure_app.py
from flask import Flask, request, render_template, redirect, url_for, session
app = Flask(__name__)
app.secret_key = "dev-secret-key"

# НЕ устанавливаем защитные флаги cookie — демонстрация уязвимости:
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = None

# Простейшая "база" пользователя
USER = {"username": "alice", "password": "password123"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if u == USER['username'] and p == USER['password']:
            session['user'] = u
            # не регенерируем сессию — для демонстрации уязвимости
            return redirect(url_for('profile'))
        return "Bad credentials", 401
    return render_template('login.html')

# Страница профиля и комментариев — здесь делаем место для XSS
comments = []

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # сохраняем комментарий как есть — это позволит сделать Stored XSS
        c = request.form.get('comment', '')
        comments.append(c)
    return render_template('profile.html', user=session['user'], comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
