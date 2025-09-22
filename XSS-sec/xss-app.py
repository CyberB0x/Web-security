from flask import Flask, request, render_template, make_response
import html

app = Flask(__name__)

# Список комментов
comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form.get("comment")
        # Исправление ошибки xss
        safe_comment = html.escape(comment)
        comments.append(safe_comment)

    response = make_response(render_template("index-xss.html", comments=comments))
    # Добавляем CSP
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


if __name__ == "__main__":
    app.run(debug=True)


