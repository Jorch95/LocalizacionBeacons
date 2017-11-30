# This Python file uses the following encoding: utf-8
import os, sys, string
from muestra import Muestra

def devolverValores():
    arch = open("datos.txt",'r')
    lines = arch.readlines()
    arreglo = [0, 0]
    if len(lines) > devolverValores.pos:
        arreglo = lines[devolverValores.pos].strip().split('-')
        devolverValores.pos = devolverValores.pos + 1
    # muestra = Muestra(float(arreglo[0]), float(arreglo[1]), float(arreglo[2]), float(arreglo[3]))
    return arreglo

devolverValores.pos = 0
