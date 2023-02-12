from proyecto import app
from flask import render_template, request, redirect, url_for
from proyecto.models import *
from datetime import datetime


def validateForm1(requestForm):
    errores=[]
    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("Tipo de moneda vacio, seleccione una moneda de la lista.") 
    if requestForm['cantidad_from'] == "" or float(requestForm['cantidad_from']) <= 0.0:
        errores.append("Cantidad negativa o nula, introduzca una cantidad positiva.")   
    if requestForm['moneda_from'] == requestForm['moneda_to']:
        errores.append("Para poder operar las monedas han de ser diferentes entre sí.")
    if requestForm['moneda_from'] == "EUR" and requestForm['moneda_to'] != "BTC" :
        errores.append("Con EUR solo puede comprar BTC.") 
    if requestForm['moneda_from'] != "BTC" and requestForm['moneda_to'] == "EUR" :
        errores.append("Para obtener EUR solo puede vender BTC.") 
    return errores


def validateForm2(requestForm,saldo):
    errores=[]
    if requestForm['moneda_from']!= 'EUR':  
        if float(requestForm['cantidad_from']) > saldo and saldo > 0:
            errores.append(f'No tiene suficiente saldo de esa moneda. El saldo actual es: {saldo}.')
        if saldo <= 0:
            errores.append('El saldo actual es nulo. No puede operar con esa moneda.')
    return errores    


def validateForm3(requestForm):
    errores=[]
    if requestForm['moneda_from'] == requestForm['moneda_to']:
        errores.append("Para poder operar las monedas han de ser diferentes entre sí.")

    if requestForm['moneda_from'] == "" or requestForm['moneda_to'] == "" :
        errores.append("Tipo de moneda vacio, seleccione una moneda de la lista.") 

    if requestForm['cantidad_from'] == "" or float(requestForm['cantidad_from']) <= 0.0 or requestForm['cantidad_to'] == "" or float(requestForm['cantidad_to']) <= 0.0:
        errores.append("Cantidad negativa o nula: Introduzca una cantidad positiva.")  
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
                precio_unitario = float(cambio(request.form['moneda_from'], request.form['moneda_to']))
                cant_from = float(request.form['cantidad_from'])
                cant_to = round(cant_from*precio_unitario,2)
                return  render_template ("purchase.html", pageTitle="Compras_Ventas_Intercambios", dataForm = request.form, cantidad_from = request.form['cantidad_from'], pu = precio_unitario, cantidad_to = cant_to, page = "Compra" )
            
            

            if 'operar' in request.form: 
                saldo = round((sum_to(request.form['moneda_from']) - sum_from(request.form['moneda_from'])),2)
                errores2 = validateForm2(request.form, saldo)
                if errores2:
                    return  render_template ("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores2,  dataForm = request.form, cantidad_from = round((sum_to(request.form['moneda_from']) - sum_from(request.form['moneda_from'])),2), page = "Compra")
            
                else:    
                    errores3= validateForm3(request.form)
                    if errores3:
                        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores3,  dataForm = request.form, cantidad_from = request.form['cantidad_from'], pu = request.form['pu'], cantidad_to = request.form['cantidad_to'], page = "Compra")
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
    invertido = round(sum_from('EUR'),2)
    recuperado = round(sum_to('EUR'),2)
    valor_compra = round(invertido - recuperado,2)
    valor_actual = saldo()
    return render_template("status.html", pageTitle="Estado", page ="Estado", invertido = invertido, recuperado = recuperado, valor_compra = valor_compra, valor_actual = valor_actual)  


                