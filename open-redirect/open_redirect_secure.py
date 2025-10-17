from flask import Flask, request, redirect, url_for, render_template, flash
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'secret'

ALLOWED_HOSTS = {
    '127.0.0.1',
    'localhost',
    # Свой домен
}

def is_safe_redirect(target: str) -> bool:
    if not target:
        return False
    parsed = urlparse(target)

    if parsed.scheme == "" and parsed.netloc == "":
        return True

    if parsed.scheme in ('http', 'https') and parsed.hostname:
        host = parsed.hostname.lower()
        if host in ALLOWED_HOSTS:
            return True

    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next') or url_for('home')

    if request.method == 'POST':
        if is_safe_redirect(next_url):
            return redirect(next_url)

        flash("Redirect blocked - target is not allowed.")
        return redirect(url_for('home'))

    return render_template('login.html', next_url=next_url)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)



