import sqlite3
from config import *

class Conexion:
    def __init__(self, querySql, params =[]):
        self.con = sqlite3.connect(ORIGIN_DATA)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySql, params)
 
    def consulta(self):
        self.filas = self.res.fetchall()
        self.columnas= self.res.description

        self.resultado = []
        for fila in self.filas:
            dato = {}
            posicion_col = 0
            for campo in self.columnas:
                dato[campo[0]]=fila[posicion_col]
                posicion_col+=1
            self.resultado.append(dato)    
        self.con.close()
        return self.resultado
    
    def suma(self, consult, columna):
        if consult == []:
            self.sum = 0.0
        else:
            self.sum = 0.0
            i = 0
            for i in range(len(consult)):
                self.sum += float(consult[i][columna])
                i+=1
        return self.sum
        
