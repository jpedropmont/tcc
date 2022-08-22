from openpyxl import load_workbook
from pandas import DataFrame
import os


class ExcelFile:
    def setWorkbook(self, file):
        self.file = file
        self.filePath = r'' + os.path.abspath(self.file.filename) + ''
        self.wb = load_workbook(self.filePath)

    def duplicateWs(self):
        originalWs = self.wb.active
        self.newWs = self.wb.copy_worksheet(originalWs)
        self.newWs.title = originalWs.title + "_new"
        self.wb.save(self.filePath)

    def process(self):
        df = DataFrame(self.newWs.values)
        df.columns = df.iloc[0]  # making first line as header
        print(df.columns)
        df = df[1:]

# Listar as colunas pro usuario, e ele decidir se vai usar
