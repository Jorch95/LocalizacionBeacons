# -- coding: utf-8 --
from flask import Flask
from flask import request
from flask import render_template
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
