import serial
from tinydb import TinyDB, where
from time import time
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

while True:
    while (arduino.inWaiting() == 0):
        pass
    ID = arduino.readline().strip()
    
    segundos = time()

    while (arduino.inWaiting() == 0):
        pass
    RSSI = arduino.readline().strip()

    tabla.insert({'ID': ID, 'RSSI': RSSI, 'segundos': segundos})
