# open_redirect_secure.py
from flask import Flask, request, redirect, url_for, render_template, abort
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

# Белый список доменов/хостов, на которые разрешён редирект (можешь добавить свои)
ALLOWED_HOSTS = {
    "127.0.0.1",       # локальный
    "localhost",
    "yourdomain.com",  # если у вас продакшн-домен
    # можно также разрешать поддомены по маске, но тут пример простой
}

def is_safe_redirect(target):
    """
    Проверяем, безопасен ли target:
    - относительные пути ("/dashboard") — безопасны
    - абсолютные URL проверяем: hostname в ALLOWED_HOSTS
    - запрещаем редиректы на неизвестные внешние хосты
    """
    if not target:
        return False

    # Если относительный путь — разрешаем
    parsed = urlparse(target)
    if parsed.scheme == "" and parsed.netloc == "":
        # относительный путь (например /dashboard) — безопасно
        return True

    # Абсолютная ссылка — проверим hostname
    host = parsed.hostname
    if host and host in ALLOWED_HOSTS:
        return True

    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    # берем next из GET или POST
    next_url = request.args.get('next') or request.form.get('next') or url_for('home')
    if request.method == 'POST':
        # безопасность: только если next_url проходит проверку — редиректим
        if is_safe_redirect(next_url):
            return redirect(next_url)
        # иначе — редиректим на домашнюю страницу или даём warning
        return redirect(url_for('home'))
    return render_template('login.html', next_url=next_url)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
