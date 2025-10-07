import os
from flask import Flask, request, render_template
from defusedxml.ElementTree import parse # безопасный парсер

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    error = None

    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            error = "Пожалуйста, выберите XML-файл"
        else:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            try:
                # Безопасный парсер defusedxml
                tree = parse(path)
                root = tree.getroot()
                data = [(child.tag, child.text) for child in root]

            except Exception as e:
                error = str(e)

    return render_template('index.html', data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
