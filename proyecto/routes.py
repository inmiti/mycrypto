from proyecto import app
from flask import render_template, request
from proyecto.models import select_all
from datetime import date    


def validateForm(requestForm):
    #hoy = date.today().isoformat()
    errores=[]
    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("tipo de moneda vacio: Seleccione una moneda de la lista")
    if requestForm['cantidad_from'] == "" or requestForm['cantidad_to'] == "":
        errores.append("cantidad vacia: Introduzca una cantidad positiva")   
    if float(requestForm['cantidad_from']) <= 0.0 or float(requestForm['cantidad_to']) <= 0.0:
        errores.append("cantidad negativa o nula: Introduzca una cantidad positiva")   
    return errores

@app.route("/")
def index():

    registros = select_all()
    return render_template("index.html", pageTitle="Movimientos", data=registros)
    

@app.route("/purchase",methods=["GET","POST"])
def purchase():
    if request.method == "GET":
        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios")
    else:
        print("esto recibo: ", request.form)
        '''
        errores = validateForm(request.form)
        if errores:
            return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores)
        else:
            return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios")
        '''
        