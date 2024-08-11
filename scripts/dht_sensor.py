from machine import Pin
import dht
import time

class DHTSensor:
  def __init__(self, pin):
    self.sensor = dht.DHT22(Pin(pin, Pin.IN, Pin.PULL_UP))

  def read(self):
    """Read temperature and humidity from the DHT22 sensor."""
    try:
      self.sensor.measure()
      temperature = self.sensor.temperature()
      humidity = self.sensor.humidity()
      heat_index = self.compute_heat_index(temperature, humidity)
      return temperature, humidity, heat_index
    except Exception as e:
      print("Error reading from DHT21:", e)
      return None, None, None

  @staticmethod
  def compute_heat_index(temperature, humidity):
      """Calcula la sensación térmica (heat index) basada en la temperatura y humedad."""
      # Convertir temperatura de Celsius a Fahrenheit
      temp_fahrenheit = (temperature * 9/5) + 32
      
      # Fórmula empírica simplificada
      hi_fahrenheit = -42.379 + 2.04901523 * temp_fahrenheit + 10.14333127 * humidity
      hi_fahrenheit -= 0.22475541 * temp_fahrenheit * humidity
      hi_fahrenheit -= 0.00683783 * temp_fahrenheit ** 2
      hi_fahrenheit -= 0.05481717 * humidity ** 2
      hi_fahrenheit += 0.00122874 * temp_fahrenheit ** 2 * humidity
      hi_fahrenheit += 0.00085282 * temp_fahrenheit * humidity ** 2
      hi_fahrenheit -= 0.00000199 * temp_fahrenheit ** 2 * humidity ** 2

      # Convertir el índice de calor de Fahrenheit a Celsius
      heat_index_celsius = (hi_fahrenheit - 32) * 5/9
      
      return heat_index_celsius
