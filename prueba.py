from openpyxl import Workbook, load_workbook
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("secretkey.json", scopes=scope)

file = gspread.authorize(creds)
workbook = file.open("Tabla de Mortalidad")
sheet = workbook.sheet1

sheet.update("C2", 5)
df = pd.DataFrame(sheet.get_all_records(head=4))
print(df)
