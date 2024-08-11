from machine import Pin, Timer, deepsleep
from network import WLAN, STA_IF
from time import sleep
from dht_sensor import DHTSensor
from uv import UVSensor
from sd import SDCard
from firebase import FirebaseManager
from ntp import NTPManager
from geolocation import GeoLocation
import config
import gc

class SensorNode:
  def __init__(self, name, led_pin, sleep_time):
    """Inicializa el nodo sensor con todos los componentes necesarios."""
    # Nombre del nodo
    self.name = name
    # Configuración del LED
    self.led_pin = Pin(led_pin, Pin.OUT)
    self.led_pin.value(1)
    self.timer = Timer(0)
    self.timer.init(period=250, mode=Timer.PERIODIC, callback=self.toggle_led)
    # Tiempo de suspension
    self.sleep_time = sleep_time
    # Configuración de la geolocalización
    self.geo_location = GeoLocation(config.api_key)
    # Configuración de sensores y utilidades
    self.dht_sensor = DHTSensor(17)
    self.uv_sensor = UVSensor(16, 22, 21)
    
    self.sd_card = SDCard(spi_sck=18, spi_mosi=23, spi_miso=19, cs_pin=5)
    self.firebase_manager = FirebaseManager(config.firebase_api_key, config.firebase_email, config.firebase_password, config.firebase_database_url)
    self.ntp_manager = NTPManager()
    sleep(1)
    self.wlan = WLAN(STA_IF)
    self.isConnected = self.wlan.isconnected()
    if self.isConnected:
      self.ntp_manager.sync_time()


  def toggle_led(self, timer):
    """Cambia el estado del LED cada 0.25 segundo."""
    self.led_pin.value(not self.led_pin.value())

  def get_position(self):
    """Obtiene la posición actual del dispositivo."""
    if not self.isConnected:
      return None, None, None
    self.geo_location.update_location()
    lat, lng = self.geo_location.get_coordinates()
    acuracy = self.geo_location.get_accuracy()
    return lat, lng, acuracy

  def collect_data(self):
    """Recopila los datos de los sensores conectados."""
    temperature, humidity, heat_index, uv_index = None, None, None, None
    for i in range(5):
      temperature, humidity, heat_index = self.dht_sensor.read()
      sleep(1)
      uv_index = self.uv_sensor.read()
    return temperature, humidity, heat_index, uv_index

  def save_data(self, current_time, temperature, humidity, heat_index, uv_index, lat, lng, acuracy):
    """Guarda en la SD y Envia a Firebase."""

    # Ver datos en consola
    #print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Thermal Sensation: {heat_index}°C")
    #print(f"UV Index: {uv_index}")
    #print(f"Position: {lat}, {lng}")
    #print(f"Accuracy: {acuracy}m")
    #print(f"Time: {current_time}")

    # Obtener nombre del archivo - con la fecha actual
    file_name = self.get_file_name()
    # Crear cadena con los datos a guardar en csv
    file_data = f"{current_time},{temperature},{humidity},{heat_index},{uv_index},{lat},{lng},{acuracy}"
    
    # Guardar datos en la tarjeta SD
    self.sd_card.write(file_name, file_data)

    # Enviar datos a Firebase si hay conexión a Internet
    if self.isConnected:
      # Autenticar con Firebase
      token = self.firebase_manager.authenticate()
      if token:
        # Esquema de datos a almacenar
        data = {
          "dateTime": f"{self.ntp_manager.get_date()} {current_time}",
          "hum": humidity,
          "light": uv_index,
          "temp": temperature,
          "heat_index": heat_index,
          "accuracy": acuracy,
          "location": {
            "lat": lat,
            "lng": lng
          }
        }
        self.firebase_manager.send_data(token, self.name, data)

  def sleep_node(self):
    """Duerme el nodo sensor por un número de segundos."""
    self.timer.deinit()
    self.led_pin.value(0)
    self.wlan.active(False)
    gc.collect()
    deepsleep(self.sleep_time * 1000)

  def get_file_name(self):
    """Obtiene el nombre del archivo para guardar los datos."""
    local_date = self.ntp_manager.get_date()
    #print(f"Fecha actual: {local_date}")
    return f"data_{local_date}.csv"


  def run(self):
    """Función principal que ejecuta el ciclo del nodo sensor."""
    #print("Iniciando nodo sensor...")
    lat, lng, acuracy = self.get_position()
    #print("Obteniendo datos de los sensores...")
    temperature, humidity, heat_index, uv_index = self.collect_data()
    #print("Obteniendo hora actual...")
    current_time = self.ntp_manager.get_time()
    #print("Guardando datos...")
    self.save_data(current_time, temperature, humidity, heat_index, uv_index, lat, lng, acuracy)
    #print("Datos guardados correctamente.")
    self.sleep_node()

if __name__ == "__main__":
    node = SensorNode()
    node.run()
