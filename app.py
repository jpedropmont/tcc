from calendar import c
from pandas import DataFrame
from openpyxl import load_workbook
from flask import Flask, request, render_template, redirect, send_from_directory, url_for
import pandas as pd
import os


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        process(f.filename)
        return redirect(request.referrer)


def process(filename):
    newWs = duplicateWs(filename)
    df = DataFrame(newWs.values)
    df.columns = df.iloc[0]  # making first line as header
    df = df[1:]
    print(df)


def duplicateWs(filename):
    filePath = r'' + os.path.abspath(filename) + ''
    wb = load_workbook(filePath)
    originalWs = wb.active
    newWs = wb.copy_worksheet(originalWs)
    newWs.title = originalWs.title + "_treated"
    wb.save(filePath)
    return newWs


if __name__ == '__main__':
    app.run(debug=True)
