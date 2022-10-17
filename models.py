from faker import Faker
from openpyxl import load_workbook
from pandas import DataFrame
from faker import Faker
from sdv.demo import load_tabular_demo
import random
import os

fake = Faker()


class ExcelFile:
    def initDataFrame(self, file):
        filePath = r'' + os.path.abspath(file.filename) + ''
        wb = load_workbook(filePath, data_only=True)
        ws = wb.active
        self.df = DataFrame(ws.values)
        self.columns = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = self.columns  # set the header row as the df header

    def getDf(self):
        return self.df

    def getColumns(self):
        return self.columns

    def process(self, form):
        # Synthesizing data
        # columns = self.getColumns().to_list()
        # amountRange = int(form['amountRange'])
        # rowsCount = len(self.df.index) - 1  # Subtract header
        # noiseAddCount = int(rowsCount * (amountRange / 100))

        # dfNoise = DataFrame(columns=columns)
        # newId = rowsCount + 1

        # for row in range(noiseAddCount):
        #     newId += 1
        #     dfNoise.loc[row] = self.generateFakeRow(columns, newId)

        # # pd.concat([self.df, dfNoise], axis=0)
        # self.df = self.df.append(dfNoise)

        # Supression
        supressedValue = form['suppressedValue']
        if supressedValue.isnumeric():
            self.df.replace([float(supressedValue)], '', inplace=True)
        else:
            self.df.replace([supressedValue], '', inplace=True)

        self.df.to_excel("output.xlsx", index=False)

        # Generalization
        generalizedColumn = form['genericColumn']
        genericValue = form['genericValue']

        self.df[generalizedColumn] = genericValue

        self.df.to_excel("output.xlsx", index=False)

    def generateFakeRow(self, columns, newId):
        row = []
        for column in columns:
            if "id" in column:
                row.append(newId)
            elif "first_name" in column:
                row.append(fake.first_name())
            elif "last_name" in column:
                row.append(fake.last_name())
            elif "name" == column:
                row.append(fake.name())
            elif "email" in column:
                row.append(fake.email())
            elif "gender" in column:
                row.append(self.randomGender())
            elif "ip" in column:
                row.append(fake.ipv4())
            else:
                row.append(fake.word())
        return row

    def randomGender(self):
        genders = ['Male', 'Female', 'Non-Binary', 'Polygender',
                   'Bigender', 'Agender', 'Genderqueer', 'Genderfluid']
        return(random.choice(genders))
