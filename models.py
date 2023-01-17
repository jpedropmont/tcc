from openpyxl import load_workbook
from pandas import DataFrame
from sdv.tabular import GaussianCopula
import os


class ExcelFile:
    def initDataFrame(self, file):
        filePath = r'' + os.path.abspath(file.filename) + ''
        wb = load_workbook(filePath, data_only=True)
        ws = wb.active
        self.df = DataFrame(ws.values)
        self.columns = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = self.columns  # set the header row as the df header
        self.initialDf = self.df

    def getDf(self, type):
        if type == "Initial":
            return self.initialDf
        elif type == "Final":
            return self.df

    def getColumns(self):
        return self.columns

    def process(self, form):
        # Supression
        supressedValue = form['suppressedValue']
        if supressedValue.isnumeric():
            self.df.replace([float(supressedValue)], '', inplace=True)
        else:
            self.df.replace([supressedValue], '', inplace=True)

        # Generalization
        generalizedColumn = form['genericColumn']
        genericValue = form['genericValue']

        self.df[generalizedColumn] = genericValue

        # Synthesizing data
        amountRange = int(form['amountRange'])
        rowsCount = len(self.df.index)
        noise = int(rowsCount * (amountRange / 100))

        model = GaussianCopula(
            anonymize_fields={
                'name': 'name',
                'home.dest': 'address',
            }
        )
        model.fit(self.df)
        self.df = model.sample(num_rows=noise)

        self.df.to_excel("output.xlsx", index=False)
