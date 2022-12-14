
from flask import Flask, request, render_template, redirect, url_for, session
from models import ExcelFile
from openpyxl import load_workbook
from pandas_profiling import ProfileReport

app = Flask(__name__)
excelFile = ExcelFile()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        excelFile.initDataFrame(file)
        return redirect(url_for('questions'))


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    columns = excelFile.getColumns()
    return render_template('questions.html', columns=columns)


@app.route('/process', methods=['GET', 'POST'])
def process():
    excelFile.process(request.form)
    return redirect(url_for('display_table'))


@app.route("/display_table")
def display_table():
    # # (B1) OPEN EXCEL FILE + WORKSHEET
    # book = load_workbook("output.xlsx")
    # sheet = book.active

    # (B2) PASS INTO HTML TEMPLATE
    profile = ProfileReport(excelFile.getDf())

    return profile.to_html()


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
