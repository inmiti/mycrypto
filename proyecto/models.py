import sqlite3
from config import *
from datetime import datetime
import requests
from proyecto.conexion import Conexion


def select_all():
    conSelect = Conexion("SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu FROM mycrypto order by date;") 
    consBD = conSelect.consulta()
    return consBD

def insert(registro):
    conInsert = Conexion("INSERT INTO mycrypto(date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu) VALUES (?,?,?,?,?,?,?)", registro)
    conInsert.con.commit()
    conInsert.con.close()
    
def cambio(monedaFrom, monedaTo):
    r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{monedaFrom}/{monedaTo}?apikey={APIKEY2}')   
    resultado = r.json()
    if r.status_code == 200:
        return resultado['rate']
    else:
        return  resultado['error']


def cambioLD(mon): 
 
    cryptos = ["EUR", "BTC", "USDT", "ETH", "BNB", "ADA", "DOT", "MATIC", "XRP", "SOL"]

    listaDict = []
    for i in cryptos:
        r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{i}/EUR?apikey={APIKEY}') 
        resultado = r.json()
        listaDict.append(resultado)

    for i in listaDict:
        if mon in i['asset_id_base']:
            pu = i['rate']
    return pu
 


def sum_from(mon):
    consult = Conexion("SELECT * FROM mycrypto where moneda_from = ?",(mon,))
    consultFrom = consult.consulta()
    sumaFrom =consult.suma(consultFrom, 'cantidad_from')
    return sumaFrom


def sum_to(mon):
    consult = Conexion("SELECT * FROM mycrypto where moneda_to = ?",(mon,))
    consultTo = consult.consulta()
    sumaTo =consult.suma(consultTo, 'cantidad_to')
    return sumaTo


def eur_monFrom():

    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM mycrypto WHERE moneda_from is NOT 'EUR'" )
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
    
    if resultado == []:
        cant = 0.0
    else:
        cant = 0.0
        i = 0
        for i in range(len(resultado)):
            pu = float(cambioLD(resultado[i]['moneda_from']))
            cant += round(pu * float(resultado[i]['cantidad_from']),2)
            i+=1
    con.close()
    return cant
    
def eur_monTo():
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM mycrypto WHERE moneda_to is NOT 'EUR'" )
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
    if resultado == []:
        cant = 0.0
    else:
        cant = 0.0
        i = 0
        for i in range(len(resultado)):
            pu = float(cambioLD(resultado[i]['moneda_to']))
            cant += round(pu * float(resultado[i]['cantidad_to']),2)
            i+=1
    con.close()
    return cant
    