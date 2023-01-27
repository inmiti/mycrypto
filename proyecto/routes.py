from proyecto import app
from flask import render_template,request
from proyecto.models import select_all

@app.route("/")
def index():
    registros = select_all()
    return render_template("index.html", pageTitle="Movimientos", data=registros)

'''
    data_tabla=[
    {'id':1, 'date':'2023-01-15','time':'14:16:01', 'moneda_from':'EUR', 'cantidad_from':3000.00, 'moneda_to':'BTC', 'cantidad_to':1.40},
    {'id':2, 'date':'2023-01-19','time':'13:46:21', 'moneda_from':'BTC', 'cantidad_from':1.00, 'moneda_to':'ECH', 'cantidad_to':50.78},
    {'id':3, 'date':'2023-01-15','time':'14:16:01', 'moneda_from':'BTC', 'cantidad_from':0.40, 'moneda_to':'EUR', 'cantidad_to':2500.00}
]
'''
    

@app.route("/purchase",methods=["GET","POST"])
def pursache():
    if request.method == "GET":
        return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios")
    else:
        return "esto es un post"