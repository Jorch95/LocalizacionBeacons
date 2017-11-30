class Muestra:
    def __init__(self, presion, temperatura, humedad, velocidad):
        self.presion = presion
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad = velocidad

    def __add__(self, otro):
        return Muestra(self.presion + otro.presion, self.temperatura + otro.temperatura, self.humedad + otro.humedad, self.velocidad + otro.velocidad)
