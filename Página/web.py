# -- coding: utf-8 --
from flask import Flask
from flask import request
from flask import render_template
<<<<<<< HEAD
from readfile import devolverValores
from muestra import Muestra

web = Flask(__name__, static_url_path='/static')

IDBeacon = "0000"
def existeID():
    global IDBeacon
    suma = Muestra(0, 0, 0, 0)
    if IDBeacon == "1234":
        auxExiste = True
    else:
        auxExiste = False
    return auxExiste

@web.route('/')
def index():
    # IDBeacon = 1234
    # existe = False
    dist = 10
    rssi = 3
    existe = existeID()
    print IDBeacon
    print existe
=======
from tinydb import TinyDB, where
from time import time
from math import sqrt

db = TinyDB('db.db')

web = Flask(__name__, static_url_path='/static')

tabla = db.table('tabla')
IDBeacon = "00000000" # Se usa para que no muestre nada apenas se entra en la página.
existe = False
# def existeID():
#     global IDBeacon
#     if IDBeacon == "12345678":
#         auxExiste = True
#     else:
#         auxExiste = False
#     return auxExiste

def consultarID():
    global IDBeacon
    global existe
    auxID = tabla.get(eid=200) #Esto está simplemente para que no haya problemas de compilación. Esto no se muestra, después se arregla.
    existeID = tabla.contains(where('ID') == IDBeacon)
    if existeID: #encontró
        # auxID = tabla.search(where('segundos') > (time() - 10)) Esto usaríamos generando los valores.
        # No pude usar esto porque el tiempo que toma en segundos como referencia el módulo time()
        # en segundos es demasiado grande en comparación a los creados en la db.
        # Calculo que justamente generandose los valores en tiempo real, no pase esto.
        auxID = tabla.get(eid=15) #Los valores de este id son los que se muestran.
        existe = True
    return auxID

intensidad1= 10.0 #Intensidad de referencia 1 por poner un valor (Sería la de referencia a un metro).
distRf = 1.0 # Distancia de referencia, o calibración, que es un metro.

def calculoDistancia(rssi): #Función de ejemplo del cálculo de la distancia.
    global intensidad1
    global distRf
    rssiN = float(rssi) #Pasa del tipo unicode a float
    dist = (distRf/(sqrt((rssiN/intensidad1))))
    return dist

@web.route('/')
def index():
    # existe = existeID()
    dist = 1 # Valores arbitrarios para que no haya error de compilación
    rssi = 100 # Lo mismo que arriba.
    global IDBeacon
    muestra = consultarID()
    if existe:
        IDBeacon = muestra['ID']
        rssi = muestra['RSSI']
        dist = calculoDistancia(muestra['RSSI'])
        #TODO agregar escala cerca-medio-lejos
>>>>>>> 5fd06225daf62e8589fab649894a9b3ccf25d8dc
    return render_template('response.html', IDBeacon=IDBeacon, distancia=dist, rssi=rssi , existe=existe)

@web.route('/', methods = ['POST'])
def action_form():
    if request.method == 'POST':
        # global IDBeacon
        data = request.form
        global IDBeacon
        IDBeacon = data["ID"]
    return index()

if __name__ == "__main__":
    # Define HOST y PUERTO para accerder
    web.run(host='localhost', port=8765)
#web.run(host='0.0.0.0', port=8765)
