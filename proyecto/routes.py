from proyecto import app
from flask import render_template, request, redirect, url_for
from proyecto.models import *
from datetime import datetime



def validateForm(requestForm):
    errores=[]
    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("tipo de moneda vacio: Seleccione una moneda de la lista")
    #if requestForm['cantidad_from'] == "" or requestForm['cantidad_to'] == "":
        #errores.append("cantidad vacia: Introduzca una cantidad positiva")   
    if requestForm['cantidad_from'] <= "" or float(requestForm['cantidad_from']) <= 0.0 or requestForm['cantidad_to'] <= "" or float(requestForm['cantidad_to']) <= 0.0:
        errores.append("cantidad negativa o nula: Introduzca una cantidad positiva")   
    
    return errores

@app.route("/")
def inicio():

    registros = select_all()
    return render_template("index.html", pageTitle="Movimientos", data=registros)
    ""

@app.route("/purchase",methods=["GET","POST"])
def operar():
    if request.method == "GET":
        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", dataForm =None)
    else:
        errores = validateForm(request.form)
        if errores:
            return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores, dataForm = request.form)
        else:
            diaHora = datetime.now()
            dia = diaHora.strftime('%Y-%m-%d')
            hora = diaHora.strftime('%H:%M:%S')
            insert([ dia, 
                        hora,
                        request.form['moneda_from'],
                        request.form['cantidad_from'],
                        request.form['moneda_to'],
                        request.form['cantidad_to'],
                        request.form['pu']])
            return redirect(url_for( 'inicio' ))
            #print("este es el registro: ",request.form, type(request.form) )
            #return "Enviar datos"
            
            
        
        
        