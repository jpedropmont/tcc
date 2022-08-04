# pip install pandas
# pip install openpyxl
# pip install inquirer

# import pandas as pd
from openpyxl import load_workbook
import inquirer
from pandas import DataFrame

print('Enter file path: ')
path = input()

if path == "":
    path = r'C:\Users\joaop\Desktop\teste.xlsx'

wb = load_workbook(path)  # loading the excel table

print('Enter worksheet name: ')
originalWsName = input()

if originalWsName == "":
    originalWsName = 'teste'

originalWs = wb[originalWsName]

newWs = wb.copy_worksheet(originalWs)

newWs.title = originalWsName + "_treated"

wb.save(path)

df = DataFrame(newWs.values)

df.columns = df.iloc[0]  # making first line as header
df = df[1:]

questionColumnsToBeTreated = [
    inquirer.Checkbox(
        "columnsToBeTreated",
        message="Which columns will be treated?",
        choices=df.columns.tolist(),
    ),
]

answerColumnsToBeTreated = inquirer.prompt(questionColumnsToBeTreated)


for column in list(answerColumnsToBeTreated['columnsToBeTreated']):
    print(column)


# questionTreatmentToBeUsed = [
    #     inquirer.Checkbox(
    #         "treatmentToBeUsed",
    #         message="Which treatment will you use for column ?",
    #         choices=["generalização de sub-árvore", "supressão de valor"],
    #     ),
    # ]
    # answerTreatment = inquirer.prompt(questionTreatmentToBeUsed)
