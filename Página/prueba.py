from tinydb import TinyDB, where
from time import time
from math import sqrt

db = TinyDB('db.db')
tabla = db.table('tabla')

IDBeacon="12345678"
auxID = tabla.all()
segundos = tabla.get(eid=1)
# existeID = tabla.contains(where('ID') == IDBeacon)
# if existeID: #encontro
rssiPromedio = 0.0
registros = tabla.search((where('ID') == IDBeacon) & (where('segundos') > (time() - float(1512016744))))
suma = 0
cant = 0
for registro in registros:
    suma += float(registro['RSSI'])
    cant += 1
    if cant == 10:
        break
print cant
print suma
if cant > 0:
    rssiPromedio =  suma/float(cant)
else:
      0

distReferencia = 1.0
rssiReferencia = 67.0
print rssiPromedio
dist = distReferencia / sqrt(rssiPromedio/rssiReferencia)
print dist