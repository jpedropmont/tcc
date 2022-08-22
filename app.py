
from flask import Flask, request, render_template, redirect, url_for
from models import ExcelFile
import pandas as pd


app = Flask(__name__)
ExcelFile = ExcelFile()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        ExcelFile.setWorkbook(file)
        ExcelFile.duplicateWs()
        return redirect(url_for('questions'))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    return render_template('questions.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    ExcelFile.process()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
