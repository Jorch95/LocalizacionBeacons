import serial
from tinydb import TinyDB, where
import time
import signal, sys

db = TinyDB('db.db')
arduino = serial.Serial('COM3', baudrate=230400, timeout=1.0)

def handler(signum, frame):
    db.close()
    arduino.close()
    print "Salida correcta"
    sys.exit()
signal.signal(signal.SIGINT, handler)

db.purge_tables()
tabla = db.table('tabla')
timeout = time.time()

while True:
    while (arduino.inWaiting() == 0):
        time.sleep(0.01)
    ID = arduino.readline().strip()

    segundos = time.time()

    while (arduino.inWaiting() == 0):
        time.sleep(0.01)
    RSSI = arduino.readline().strip()

    tabla.insert({'ID': ID, 'RSSI': RSSI, 'segundos': segundos})

    #cada 60 segundos, se borraran las muestras tomadas hace mas de 60 segundos
    if (segundos - timeout) > 60:
        tabla.remove(where('segundos') < (segundos - 60))
        timeout = segundos
