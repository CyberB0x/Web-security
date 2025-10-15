from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next') or url_for('home')
    if request.method == 'POST':
        return redirect(next_url)
    return render_template('login.html', next_url=next_url)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)