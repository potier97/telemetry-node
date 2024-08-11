from machine import Pin, SoftI2C

class UVSensor:
  def __init__(self, power_pin, scl_pin, sda_pin):
    self.power_pin = Pin(power_pin, Pin.OUT)
    self.power_pin.value(1)
    self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
    self.address_low = 0x38
    self.address_high = 0x39
    # Configurar el sensor (cambiar el modo de integración)
    # 0x02 = Modo de integración normal
    # 0x06 = Modo de integración largo (aumenta sensibilidad)
    self.i2c.writeto(self.address_low, bytes([0x02]))

  def read(self):
    """Read UV index from the VEML6070 sensor."""
    try:
      data_low = self.i2c.readfrom(self.address_low, 1)
      data_high = self.i2c.readfrom(self.address_high, 1)
      uv_index = (data_high[0] << 8) | data_low[0]
      return uv_index
    except Exception as e:
      print("Error reading from VEML6070:", e)
      return None
