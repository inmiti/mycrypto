from proyecto import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", pageTitle="Movimientos")

@app.route("/purchase")
def pursache():
    return render_template("purchase.html", pageTitle="Compras_Ventas_Intercambios")