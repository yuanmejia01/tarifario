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

df = pd.DataFrame(sheet.get_all_records(head=4))
print(df)
lista = ['seguro_sobrevivencia', '45', 'masculino', '45', '10', 'anual', '1', '4', '0', 'unico', 'anticipado']
def PPU_unica(lista):
    global sheet
    #Cobertura de sobrevivencia
    if lista[0] == "seguro_sobrevivencia":
        #Unico
        if lista[4] == "1":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x

            E = list(df["Dx"])[x+h]/list(df["Dx"])[x]
            PPU = E * float(lista[6])
        #Vitalicio
        elif lista[4] == "100":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x

            a = list(df["Nx"])[x+h]/list(df["Dx"])[x]
            PPU = a * float(lista[6])
        #Temporal
        else:
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x
            n = int(lista[4])
            if x+n > 100:
                a = list(df["Nx"])[x + h] / list(df["Dx"])[x]
            else:
                a = (list(df["Nx"])[x+h] - list(df["Nx"])[x+h+n])/list(df["Dx"])[x]
            PPU = a * float(lista[6])

    #Cobertura de muerte
    else:
        #Unico pago
        if lista[4] == "1":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x

            A = list(df["Cx"])[x + h] / list(df["Cx"])[x]
            PPU = A * float(lista[6])

        #Vitalicio
        elif lista[4] == "100":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x
            n = int(lista[4])
            A = (list(df["Mx"])[x + h - 1]) / list(df["Dx"])[x]
            PPU = A * float(lista[6])
        #Temporal
        else:
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x
            n = int(lista[4])
            a = (list(df["Mx"])[x + h] - list(df["Mx"])[x + h + n + 1]) / list(df["Dx"])[x]
            PPU = a * float(lista[6])
        return round(PPU, 2)



print(float(sheet.acell("C2").value))