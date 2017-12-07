# -- coding: utf-8 --
from flask import Flask
from flask import request
from flask import render_template
from tinydb import TinyDB, where
import time
from math import sqrt

db = TinyDB('db.db')

web = Flask(__name__, static_url_path='/static')

tabla = db.table('tabla')
tablaReferencias = db.table('referencias')
IDBeacon = "00000000" # Se usa para que no muestre nada apenas se entra en la página.
intervalo = 100000.0
IDCalibrado = "00000000" #Se usa para ver la funcionalidad del botón calibrar.

#busca el "ID" recibido en la tabla de referencias. si lo encuentra lo devuelve, sino devuelve 0 (seria ilogico que un RSSI de ref sea 0).
def obtenerReferenciaRSSSI(ID):
    referencia = tablaReferencias.search(where('ID') == ID)
    if len(referencia) == 1:
        return referencia[0]['RSSIref']
    else:
        return 0

#calcula el promedio de RSSIs escaneados correspondientes a "ID" en un lapso de "duracion"
def obtenerPromedioRSSI(ID, duracion):
    registros = tabla.search((where('ID') == ID) & (where('segundos') > (time.time() - float(duracion))))
    suma = 0
    cant = 0
    for registro in registros:
        suma += int(registro['RSSI'])
        cant += 1
    if cant > 0:
        return float(suma)/float(cant)
    else:
        return 0

def calculoDistancia(rssiPromedio, rssiReferencia):
    distReferencia = 1.0
    dist = 10. ** ((rssiPromedio - rssiReferencia) / 40)
    return dist

#En base a la distancia aproximada determinada, se diferencia la proximidad del Beacon entre 
#"Cerca", "Medianamente cerca" y "Lejos".
def calculoProximidad(distancia):
    LimMaxC=2.0
    LimMaxM=5.0
    if distancia > LimMaxC and distancia < LimMaxM:
        return "Medianamente cerca"
    elif distancia <= LimMaxC:
        return "Cerca"
    else:
        return "Lejos"

#al llamar a este metodo se asume que el celular esta a 1m.
#se toman muestras del RSSI de "ID" durante 40seg, se calcula su promedio y se lo guarda en la tabla de referencias de RSSIs
#devuelve el valor de referencia almacenado por si acaso sea de utilidad
def calibrar(ID):
    time.sleep(40)
    rssiPromedio = obtenerPromedioRSSI(ID, 40)
    tablaReferencias.remove(where('ID') == ID)
    tablaReferencias.insert({'ID': ID, 'RSSIref': rssiPromedio})
    return index()

@web.route('/')
def index():
    global IDBeacon
    global intervalo
    calibrado = False
    dist = 99999.99
    rssiPromedio = obtenerPromedioRSSI(IDBeacon, intervalo)
    rssiReferencia = obtenerReferenciaRSSSI(IDBeacon)
    if rssiReferencia > 0:
        calibrado = True
        if rssiPromedio > 0:
            dist = calculoDistancia(rssiPromedio, rssiReferencia)
            proximidad = calculoProximidad(dist)
    return render_template('response.html', IDBeacon=IDBeacon, distancia=dist, rssi=rssiPromedio , calibrado=calibrado, acercamiento=proximidad)

@web.route('/', methods = ['POST'])
def action_form():
    if request.method == 'POST':
        data = request.form
        global IDBeacon
        global intervalo
        IDBeacon = data["ID"]
        intervalo = data["seg"]
        return index()

@web.route('/calibrador', methods = ['POST'])
def calibrador():
    if request.method == 'POST':
        global IDBeacon
        return calibrar(IDBeacon)

if __name__ == "__main__":
    # Define HOST y PUERTO para accerder
    web.run(host='localhost', port=8765)
#web.run(host='0.0.0.0', port=8765)
