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
        errores = validateForm1(request.form)
        if errores:
            return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores, dataForm = request.form)
        else:
            if 'calcular' in request.form:
                print(cambio(request.form['moneda_from']))
                return "llamada a api"
              
                
                
                '''
                  #print( cambio(request.form['moneda_from'],request.form['moneda_to']))

                cant_to = float(request.form['cantidad_from'])* float(precio_unit)
                cant_to_str = str(cant_to)
                list_form = {
                    'moneda_from' : request.form['moneda_from'],
                    'moneda_to' : request.form['moneda_to'],
                    'cantidad_from' : request.form['cantidad_form'],
                    'cantidad_to' : cant_to_str,
                    'pu' : precio_unit
                }
                
                return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios", msgError=errores, dataForm = list_form)
            
            
            if 'operar' in request.form:
                return 'guardar en sqlite'
            
            else:

            
                precio_unit = get_pu(request.form['moneda_from'],request.form['moneda_to'])
                cant_to = float(request.form['cantidad_from'])/precio_unit
                diaHora = datetime.now()
                dia = diaHora.strftime('%Y-%m-%d')
                hora = diaHora.strftime('%H:%M:%S')
                
                insert([ dia, 
                            hora,
                            request.form['moneda_from'],
                            request.form['cantidad_from'],
                            request.form['moneda_to'],
                            request.form['cantidad_to'],
                            precio_unit])

            return redirect(url_for( 'inicio' ))
            
        
           
            #print("este es el registro: ",request.form, type(request.form) )
            #return "Enviar datos"

'''