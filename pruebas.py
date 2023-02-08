import requests
import sqlite3
from config import *
from datetime import datetime



con = sqlite3.connect(ORIGIN_DATA)
cur = con.cursor()
res = cur.execute("SELECT * FROM mycrypto where moneda_to = 'ADA'")  

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

print(resultado)
if resultado == []:    
    sumaT = 0.0
else: 
    sumaT = 0.0
    i = 0
    for i in range(len(resultado)):
        sumaT += float(resultado[i]['cantidad_to'])
        i+=1

con.close()
print(sumaT, type(sumaT))