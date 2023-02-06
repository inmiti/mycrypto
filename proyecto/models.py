import sqlite3
from config import *
from datetime import datetime
import requests

def select_all():
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res = cur.execute("SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu FROM mycrypto order by date")
    filas = res.fetchall()
    columnas= res.description

    resultado = []

    for fila in filas:
        dato = {}
        posicion_col = 0
        for campo in columnas:
            dato[campo[0]]=fila[posicion_col]
            posicion_col+=1
        resultado.append(dato)
    
    con.close()
    return resultado

def insert(registro):

    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    res = cur.execute("INSERT INTO mycrypto(date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu) VALUES (?,?,?,?,?,?,?)", registro)
    con.commit()
    con.close()
    
def cambio(monedaFrom, monedaTo):

    r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{monedaFrom}/{monedaTo}?apikey={APIKEY}')
    
    resultado = r.json()

    if r.status_code == 200:
        return resultado['rate']
    else:
        return  resultado['error']
   
def sum_from(mon):
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM mycrypto where moneda_from = ?",(mon,) )
    filas = res.fetchall() #obtengo filas en tupla
    columnas= res.description
    resultado = []
    for fila in filas:
        dato = {}
        posicion_col = 0
        for campo in columnas:
            dato[campo[0]]=fila[posicion_col]
            posicion_col+=1
            resultado.append(dato)
    suma = 0.0
    i = 0
    for i in range(len(resultado)):
        suma += float(resultado[i]['cantidad_from'])
        i+=1
    con.close()
    return suma


def sum_to(mon):
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res_from = cur.execute("SELECT * FROM mycrypto where moneda_to = ?",(mon,) )
    
    filas_from = res_from.fetchall() #obtengo filas en tupla
    columnas_from= res_from.description
    
    resultado = []
    
    for fila in filas_from:
        dato = {}
        posicion_col = 0
        
        for campo in columnas_from:
            dato[campo[0]]=fila[posicion_col]
            posicion_col+=1

        resultado.append(dato)

    suma = 0.0
    i = 0
    for i in range(len(resultado)):
        suma += float(resultado[i]['cantidad_to'])
        i+=1
    
    con.close()
    return suma
