#Importando las librerias
import mpld3
from flask import Flask, render_template, request, session, escape, redirect, url_for, flash
from flask_sqlalchemy import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import math
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
sheet.update("C2", 0.04)


def PPU_unica(lista):
    global sheet
    # Cobertura de sobrevivencia
    if lista[0] == "Sobrevivencia":
        # Unico
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
        # Vitalicio
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
        # Temporal
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
            if (lista[8] == "" or lista[8] == "0"):
                if x+n > 100:
                    a = list(df["Nx"])[x + h] / list(df["Dx"])[x]
                else:
                    a = (list(df["Nx"])[x+h] - list(df["Nx"])[x+h+n])/list(df["Dx"])[x]
                PPU = a * float(lista[6])
            else:
                crecimiento = float(lista[8])
                E = 0
                for i in range(n):
                    E += ((1+crecimiento/100)**i) * list(df["Dx"])[x+h+i]/list(df["Dx"])[x]
                PPU = E * float(lista[6])
        return PPU
    #Cobertura de muerte
    else:
        i = float(sheet.acell("C2").value)
        if lista[5] == "Al final del año":
            k = 1
        elif lista[5] == "Al final del semestre":
            k = 2
        elif lista[5] == "Al final del cuatrimestre":
            k = 3
        elif lista[5] == "Al final del trimestre":
            k = 4
        elif lista[5] == "Al final del bimestre":
            k = 6
        else:
            k = 12
        j = ((1+i)**(1/k)) - 1
        j = j * k
        factorij = i/j
        # Unico pago
        if lista[4] == "1":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x

            A = list(df["Cx"])[x + h] / list(df["Dx"])[x]
            PPU = A * float(lista[6]) * factorij

        # Vitalicio
        elif lista[4] == "100":
            if lista[2] == "masculino":
                sheet = workbook.sheet1
                df = pd.DataFrame(sheet.get_all_records(head=4))
            else:
                sheet = workbook.worksheet("Mujeres")
                df = pd.DataFrame(sheet.get_all_records(head=4))
            x = int(lista[1])
            h = int(lista[3]) - x
            A = (list(df["Mx"])[x + h - 1]) / list(df["Dx"])[x]
            PPU = A * float(lista[6]) * factorij
        # Temporal
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
            A = (list(df["Mx"])[x + h] - list(df["Mx"])[x + h + n + 1]) / list(df["Dx"])[x]
            PPU = A * float(lista[6]) * factorij
        return PPU



app = Flask(__name__)  # __name__ es una variable que almacena el nombre de nuestro archivo
#[tipo_seguro, edad, genero, edad se empezara a pagar la SA, cantidad años cobertura, cuando recibir el pago, SA, interes tecnico, Crecimiento SA, Frecuencia de pago]
#Excepcion para la regresion lineal y poisson
def PPA(ppu, edad, pago, genero):
    ppa_fraccionada = 0
    if genero == "masculino":
        sheet = workbook.sheet1
        df = pd.DataFrame(sheet.get_all_records(head=4))
    else:
        sheet = workbook.worksheet("Mujeres")
        df = pd.DataFrame(sheet.get_all_records(head=4))
    x = int(edad[1])
    if pago[1] == "anticipado":
        h = 0
    else:
        h = 1
    n = int(pago[2])
    E = list(df["Dx"])[x + n + h] / list(df["Dx"])[x + h]
    if x + n > 100:
        a = list(df["Nx"])[x + h] / list(df["Dx"])[x + h]
    else:
        a = (list(df["Nx"])[x + h] - list(df["Nx"])[x + h + n]) / list(df["Dx"])[x + h]
    if pago[0] == "unico":
        ppa_anual = ppu/1
        ppa_fraccionada = ppa_anual
    # Anual
    else:
        ppa_anual = ppu/a
        if pago[0] == "1":
            ppa_anual = ppa_anual
            ppa_fraccionada = ppa_anual
    # Semestral
        else:
            k = int(pago[0])
            factor = (k-1)/(2*k)
            a_nueva = a - (factor*(1-E))
            ppa_anual = ppu/a_nueva
            ppa_fraccionada = ppa_anual/k
    return ppa_anual, ppa_fraccionada

def PT(ppa, gastos, edad, genero, pago, SA):
    ad_sa = float(gastos[0])
    ad_pt = float(gastos[1])
    ge_sa = float(gastos[2])
    ge_pt = float(gastos[3])
    li_sa = float(gastos[4])
    li_pt = float(gastos[5])

    if genero == "masculino":
        sheet = workbook.sheet1
        df = pd.DataFrame(sheet.get_all_records(head=4))
    else:
        sheet = workbook.worksheet("Mujeres")
        df = pd.DataFrame(sheet.get_all_records(head=4))
    x = int(edad[1])
    if pago[1] == "anticipado":
        h = 0
    else:
        h = 1
    n = int(pago[2])
    E = list(df["Dx"])[x + n + h] / list(df["Dx"])[x + h]
    if x + n > 100:
        a = list(df["Nx"])[x + h] / list(df["Dx"])[x + h]
    else:
        a = (list(df["Nx"])[x + h] - list(df["Nx"])[x + h + n]) / list(df["Dx"])[x + h]
    gastos_sa = [ppa, ad_sa/a, SA * li_sa *E / a, ge_sa]
    gastos_pt = [ad_pt/a, SA * li_pt * E / a, ge_pt]
    return round(sum(gastos_sa)/(1 - sum(gastos_pt)), 2)
#Creando rutas
#Ruta base
@app.route("/")
def index():
    # Creando algunas varibles que usaremos luego
    global lista_cobertura, nombre, todas_coberturas, resultados, df_resultados, gastos, forma_pago
    todas_coberturas = []
    resultados = []
    gastos = list()
    forma_pago = []
    df_resultados = pd.DataFrame(columns=["Tipo Cobertura", "Edad", "Género",
                                          "Edad comienzo de la cobertura", "Cantidad de Años Cobertura",
                                          "Recibir el pago",
                                          "Suma Asegurada", "Interés Técnico", "Crecimiento", "Frecuencia"])
    return redirect(url_for('inicio'))


#Inicio
@app.route("/tarifario", methods=["GET", "POST"])
def inicio():
    global mensaje, nombre
    if request.method == "POST":
        if request.form["tasa"] == "":
            pass
        else:
            sheet.update("C2", float(request.form["tasa"])/100)
        if request.form["tipo_seguro"] == "Sobrevivencia":
            lista_cobertura = [request.form["tipo_seguro"], request.form["edad"], request.form["genero"],
                               request.form["edad_sa"], request.form["cober"], "Al final del año",
                               request.form["suma_asegurada"], request.form["tasa"], request.form["crecimiento_sa"],
                               request.form["frecuencia"]]

        else:
            lista_cobertura = [request.form["tipo_seguro"], request.form["edad"], request.form["genero"],
                               request.form["edad_sa"], request.form["cober"], request.form["recibir_pago"],
                               request.form["suma_asegurada"], request.form["tasa"], "0",
                               request.form["frecuencia"]]
        nombre = request.form["fname"]
        gastos.append([request.form["ad_sa"], request.form["ad_pt"], request.form["ge_sa"],
                       request.form["ge_pt"], request.form["li_sa"], request.form["li_pt"]])
        forma_pago.append([request.form["frecuencia"], request.form["modopago"], request.form["años_pagando"]])
        todas_coberturas.append(lista_cobertura)
        if request.form["otracobertura"] == "si":
            return redirect(url_for("inicio"))
        else:
            for i in range(len(todas_coberturas)):
                df_resultados.loc[len(df_resultados)] = todas_coberturas[i]
                resultados.append(PPU_unica(todas_coberturas[i]))
            df_resultados["PPU"] = resultados
            print(df_resultados)
            sumaPPU = sum(df_resultados["PPU"])
            ppa_anual, ppa_fraccionada = PPA(sumaPPU, todas_coberturas[0][1], forma_pago[0], todas_coberturas[0][2])
            sumaSA = (float(todas_coberturas[0][4]) * float(todas_coberturas[0][6]))
            prima_tarifa = PT(ppa_anual, gastos[0], todas_coberturas[0][1], todas_coberturas[0][2], forma_pago[0], sumaSA)

            if ppa_fraccionada == ppa_anual:
                mensaje = "PPA Anual: {:,.2f}".format(ppa_anual) + "\n" + \
                          "Prima de Tarifa Anual: {:,.2f}".format(prima_tarifa)
            else:
                mensaje = "PPA Anual: {:,.2f}".format(ppa_anual) + "\n" + \
                          "PPA Fraccionada: {:,.2f}".format(ppa_fraccionada) + "\n"\
                          "Prima de Tarifa Anual: {:,.2f}".format(prima_tarifa) + "\n"\
                          + "Prima de Tarifa Fraccionada: {:,.2f}".format(prima_tarifa/int(ppa_anual/ppa_fraccionada))
            return redirect(url_for("prueba"))
    return render_template("form.html")


#Ruta prueba
@app.route("/prueba", methods=["GET", "POST"])
def prueba():
    mostrar = df_resultados
    mostrar["PPU"] = mostrar["PPU"].map('{:,.2f}'.format)
    mostrar["Suma Asegurada"] = mostrar["Suma Asegurada"].astype(float)
    mostrar = mostrar.drop("Frecuencia", axis=1)
    mostrar['Género'] = mostrar['Género'].str.capitalize()
    mostrar['Interés Técnico'] = mostrar['Interés Técnico'] + "%"
    mostrar['Crecimiento'] = mostrar['Crecimiento'] + "%"
    mostrar["Suma Asegurada"] = mostrar["Suma Asegurada"].map('{:,.2f}'.format)
    print(mensaje)
    return render_template("table.html", mensaje=mensaje, nombre=nombre, tables = [mostrar.to_html(classes="table-bordered", index=False, justify="center")])

#Iniciar la aplicacion
if __name__ == "__main__":
    app.run(debug=True)
