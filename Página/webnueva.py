# -- coding: utf-8 --
from flask import Flask
from flask import request
from flask import render_template
from tinydb import TinyDB, where
from time import time
from math import sqrt

db = TinyDB('db.db')

web = Flask(__name__, static_url_path='/static')

tabla = db.table('tabla')
tablaReferencias = db.table('referencias')
IDBeacon = "00000000" # Se usa para que no muestre nada apenas se entra en la página.
intervalo = 0.0

def obtenerReferenciaRSSSI():
    #leer desde archivo o calcular con muestras actuales
    return 67

def obtenerPromedioRSSI(intervalo):
    registros = tabla.search((where('ID') == IDBeacon) & (where('segundos') > (time() - float(intervalo))))
    suma = 0
    cant = 0
    for registro in registros:
        suma += registro['RSSI']
        cant += 1
    print cant
    print suma
    if cant > 0:
        return suma/float(cant)
    else:
        return 0

def calculoDistancia(rssiPromedio, rssiReferencia):
    distReferencia = 1.0
    dist = distReferencia / sqrt(rssiPromedio/rssiReferencia)
    return dist

@web.route('/')
def index():
    calibrado = False
    rssiPromedio = obtenerPromedioRSSI(intervalo)
    rssiReferencia = obtenerReferenciaRSSSI(IDBeacon)
    if rssiReferencia > 0:
        calibrado = True
    if rssiPromedio > 0:
        dist = calculoDistancia(rssiPromedio, rssiReferencia)
        #TODO agregar escala cerca-medio-lejos
        if rssi > 0:
            return render_template('response.html', IDBeacon=IDBeacon, distancia=dist, rssi=rssiPromedio , existe=True, calibrado=calibrado)
    else:
        return render_template('response.html', IDBeacon=IDBeacon, distancia="Desconocida", rssi=rssiPromedio , existe=False, calibrado=calibrado)

@web.route('/', methods = ['POST'])
def action_form():
    if request.method == 'POST':
        # global IDBeacon
        data = request.form
        global IDBeacons
        IDBeacon = data["ID"]
        global intervalo
        intervalo = data["seg"]
    return index()

if __name__ == "__main__":
    # Define HOST y PUERTO para accerder
    web.run(host='localhost', port=8765)
#web.run(host='0.0.0.0', port=8765)
