# -- coding: utf-8 --
from flask import Flask
from flask import request
from flask import render_template
from tinydb import TinyDB, where
from math import sqrt
import time

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
        return referencia['RSSIref']
    else:
        return 51

#calcula el promedio de RSSIs escaneados correspondientes a "ID" en un lapso de "duracion"
def obtenerPromedioRSSI(ID, duracion):
    registros = tabla.search((where('ID') == ID) & (where('segundos') > (time() - float(duracion))))
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
    dist = sqrt(rssiPromedio/rssiReferencia)
    return dist

#al llamar a este metodo se asume que el celular esta a 1m.
#se toman muestras del RSSI de "ID" durante 15seg, se calcula su promedio y se lo guarda en la tabla de referencias de RSSIs
#devuelve el valor de referencia almacenado por si acaso sea de utilidad
def calibrar(ID):
    time.sleep(15)
    rssiPromedio = obtenerPromedioRSSI(ID, 15)
    tablaReferencias.insert({'ID': ID, 'RSSIref': rssiPromedio})
    return rssiPromedio

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
    #TODO agregar escala cerca-medio-lejos
    return render_template('response.html', IDBeacon=IDBeacon, distancia=dist, rssi=rssiPromedio , calibrado=calibrado, intervalo=intervalo, IDCalibrado = IDCalibrado)

@web.route('/', methods = ['POST'])
def action_form():
    if request.method == 'POST':
        data = request.form
        global IDBeacon
        global intervalo
        IDBeacon = data["ID"]
        intervalo = data["seg"]
    return index()

if __name__ == "__main__":
    # Define HOST y PUERTO para accerder
    web.run(host='localhost', port=8765)
#web.run(host='0.0.0.0', port=8765)
