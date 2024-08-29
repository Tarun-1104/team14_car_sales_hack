from flask import Flask, render_template, request, jsonify
import os
from models.extract import extract_information

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            extracted_data = extract_information(filepath)
            return jsonify(extracted_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)