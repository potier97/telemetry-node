from machine import Pin, SoftI2C

veml6070Pin = Pin(16, Pin.OUT)
veml6070Pin.value(1)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  # Usa SoftI2C si es necesario
devices = i2c.scan()


if devices:
    print("Dispositivos I2C encontrados:", devices)
else:
    print("No se encontraron dispositivos I2C")
