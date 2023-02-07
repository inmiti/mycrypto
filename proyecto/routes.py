from proyecto import app
from flask import render_template, request, redirect, url_for
from proyecto.models import *
from datetime import datetime


def validateForm1(requestForm):
    errores=[]
    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("tipo de moneda vacio: Seleccione una moneda de la lista")
    #if requestForm['cantidad_from'] == "" or requestForm['cantidad_to'] == "":
        #errores.append("cantidad vacia: Introduzca una cantidad positiva")   
    if requestForm['cantidad_from'] == "" or float(requestForm['cantidad_from']) <= 0.0:
        errores.append("cantidad negativa o nula: Introduzca una cantidad positiva")   
    return errores

def validateForm2(requestForm):
    errores=[]
    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("tipo de moneda vacio: Seleccione una moneda de la lista") 
    if requestForm['cantidad_from'] == "" or float(requestForm['cantidad_from']) <= 0.0 or requestForm['cantidad_to'] == "" or float(requestForm['cantidad_to']) <= 0.0:
        errores.append("cantidad negativa o nula: Introduzca una cantidad positiva")  
    if requestForm['pu'] !=  cambio(requestForm['moneda_from'], requestForm['moneda_to']): #or requestForm['cantidad_to'] != round(float(request.form['cantidad_from'])*cambio(requestForm['moneda_from'], requestForm['moneda_to']),2):
        errores.append('pulse calcular antes de operar')
    return errores

@app.route("/")
def inicio():
    registros = select_all()
    return render_template("index.html", pageTitle="Movimientos", data=registros, page = "Inicio")
    ""

@app.route("/purchase",methods=["GET","POST"])
def operar():
    if request.method == "GET":
        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", dataForm =None, pu = None, page = "Compra")
    else:
        errores = validateForm1(request.form)
        if errores:
            return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores,  dataForm = request.form, cantidad_from = request.form['cantidad_from'], page = "Compra")
        else:
            if 'calcular' in request.form:
                precio_unitario = cambio(request.form['moneda_from'], request.form['moneda_to'])
                cant_to = round(float(request.form['cantidad_from'])*precio_unitario,2)
                return  render_template ("purchase.html", pageTitle="Compras_Ventas_Intercambios", dataForm = request.form, cantidad_from = request.form['cantidad_from'], pu = precio_unitario, cantidad_to = cant_to, page = "Compra" )
      
            if 'operar' in request.form: 
                if request.form['moneda_from']!= 'EUR' and ( float(request.form['cantidad_from']) > ( sum_to(request.form['moneda_from']) - sum_from(request.form['moneda_from']) ) ):
                    mensaje = ['No tiene suficiente saldo de esa moneda. Para poder operar la Q(From) ha de ser inferior al saldo actual:', round((sum_to(request.form['moneda_from']) - sum_from(request.form['moneda_from'])),2)]
                    return  render_template ("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=mensaje,  dataForm = request.form, cantidad_from = round((sum_to(request.form['moneda_from']) - sum_from(request.form['moneda_from'])),2), page = "Compra")
                
                else:    
                    errores2= validateForm2(request.form)
                    if errores2:
                        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores2,  dataForm = request.form, cantidad_from = request.form['cantidad_from'], page = "Compra")
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

@app.route("/status")
def resumen():
    #print(sum_to('DOT'), type(sum_to('DOT')), sum_from('DOT'), sum_from('DOT') - sum_to('DOT') )
    #return "ver suma moneda from"
    return render_template("status.html", pageTitle="Estado")  


                