import random

def tomarMuestra():
    arch = open("datos.txt",'a')
    presion = random.randrange(101)
    temperatura = random.randrange(0,30)
    humedad = random.randrange(60,95) #Si estamos en La Plata.
    velocidadViento = random.randrange(60,120)
    secuencia = (presion, temperatura, humedad, velocidadViento)
    s = '-'.join(str(v) for v in secuencia)
    arch.write(s)
    arch.write("\n")
    arch.close()
