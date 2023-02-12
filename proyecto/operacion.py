from proyecto.conexion import Conexion

class SumaMonDict:
    def __init__(self, consulta,campo_mon, campo_cant):
        self.consulta = consulta
        self.campo_mon = campo_mon
        self.campo_cant = campo_cant
        self.dictMon = { "EUR":0.0, "BTC":0.0, "USDT":0.0, "ETH":0.0, "BNB":0.0, 
                           "ADA":0.0, "DOT":0.0, "MATIC":0.0, "XRP":0.0, "SOL":0.0}
    
    def dictSum(self):
        if self.consulta == []:
            self.dictMon = { "EUR":0.0, "BTC":0.0, "USDT":0.0, "ETH":0.0, "BNB":0.0, 
                    "ADA":0.0, "DOT":0.0, "MATIC":0.0, "XRP":0.0, "SOL":0.0}
        else:
            for mon in self.dictMon:
                i = 0
                for i in range(len(self.consulta)):
                    if mon == self.consulta[i][self.campo_mon]:
                        self.dictMon[mon] += self.consulta[i][self.campo_cant]
                        i += 1
        return self.dictMon
    
