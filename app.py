
from flask import Flask, request, render_template, redirect, url_for, session
from models import ExcelFile
import sweetviz as sv

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
    return redirect(url_for('report'))


@app.route("/report")
def report():
    initial = excelFile.getDf("Initial")
    final = excelFile.getDf("Final")

    feature_config = sv.FeatureConfig(skip=["ticket", "boat", "body"])
    my_report = sv.compare([initial, 'Initial'], [
                           final, 'Final'], feat_cfg=feature_config)
    my_report.show_html()

    return ""


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
