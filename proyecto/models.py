from config import *
import requests
from proyecto.conexion import Conexion
from proyecto.operacion import SumaMonDict


def select_all():
    conSelect = Conexion("SELECT date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu FROM mycrypto order by date;") 
    consBD = conSelect.consulta()
    return consBD

def insert(registro):
    conInsert = Conexion("INSERT INTO mycrypto(date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, pu) VALUES (?,?,?,?,?,?,?)", registro)
    conInsert.con.commit()
    conInsert.con.close()
    
def cambio(monedaFrom, monedaTo):
    r = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{monedaFrom}/{monedaTo}?apikey={APIKEY}')   
    resultado = r.json()
    if r.status_code == 200:
        return resultado['rate']
    else:
        return  resultado['error']


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


def dict_monFrom():
    conectFrom = Conexion("SELECT * FROM mycrypto WHERE moneda_from is NOT 'EUR'")
    consult = conectFrom.consulta()
    diccionario = SumaMonDict(consult,'moneda_from','cantidad_from' )
    dicMon = diccionario.dictSum()
    return dicMon

 
def dict_monTo():
    conect = Conexion("SELECT * FROM mycrypto WHERE moneda_to is NOT 'EUR'")
    consult = conect.consulta()
    diccionario = SumaMonDict(consult,'moneda_to','cantidad_to')
    dicMon = diccionario.dictSum()
    return dicMon


def saldo():
    dictMon = { "EUR":0.0, "BTC":0.0, "USDT":0.0, "ETH":0.0, "BNB":0.0, 
                    "ADA":0.0, "DOT":0.0, "MATIC":0.0, "XRP":0.0, "SOL":0.0}
    dictMonFrom = dict_monFrom()
    dictMonTo = dict_monTo()

    for monTo in dictMonTo:
        for monFrom in dictMonFrom:
            if monTo == monFrom:
                dictMon[monTo] = dictMonTo[monTo] - dictMonFrom[monFrom]
    eurTot = 0.0
    for mon in dictMon:
        if dictMon[mon] == 0.0:
            eurTot += 0.0
        if dictMon[mon] != 0.0:
            eurTot += round(dictMon[mon]* cambio(mon, 'EUR'),2)
    return eurTot
  
