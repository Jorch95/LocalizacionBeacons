from tinydb import TinyDB, where
from time import time

db = TinyDB('db.db')
tabla = db.table('tabla')

IDBeacon="12345678"
auxID = tabla.all()
segundos = tabla.get(eid=1)
# existeID = tabla.contains(where('ID') == IDBeacon)
# if existeID: #encontro
auxID = tabla.search(where('segundos') > (time()))
existe = True
cant = tabla.count(where('segundos') < (time() - segundos['segundos']))
print cant
print time()
print segundos['ID']