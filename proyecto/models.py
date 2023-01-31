import sqlite3
from config import *
from datetime import datetime
import requests

def select_all():
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res = cur.execute("SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to FROM mycrypto order by date")
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
    
def cambio(monedaF):
    
    r = requests.get('https://rest.coinapi.io/v1/exchangerate/EUR/BTC?apikey={APIKEY}')
    
    resultado = r.json()
    precio_unitario = resultado['rate']

    return precio_unitario
   
