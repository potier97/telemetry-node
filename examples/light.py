from machine import Pin, SoftI2C
import time

class VEML6070:
    def __init__(self, i2c):
        self.i2c = i2c
        self.address_low = 0x38  # Dirección I2C para lectura baja
        self.address_high = 0x39 # Dirección I2C para lectura alta

        # Configurar el sensor (cambiar el modo de integración)
        # 0x02 = Modo de integración normal
        # 0x06 = Modo de integración largo (aumenta sensibilidad)
        self.i2c.writeto(self.address_low, bytes([0x02]))  # Modo de integración normal

    def read_uv(self):
        # Leer datos UV (2 bytes)
        data_low = self.i2c.readfrom(self.address_low, 1)
        data_high = self.i2c.readfrom(self.address_high, 1)

        # Combinar bytes altos y bajos
        uv_index = (data_high[0] << 8) | data_low[0]
        return uv_index

veml6070Pin = Pin(16, Pin.OUT)
veml6070Pin.value(1)

# Inicializar el I2C y el sensor
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
uv_sensor = VEML6070(i2c)

def test_uv_sensor():
    try:
        uv_index = uv_sensor.read_uv()
        print("UV Index: {}".format(uv_index))
    except Exception as e:
        print("Error reading from VEML6070:", e)

while True:
    test_uv_sensor()
    time.sleep(5)
