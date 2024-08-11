from machine import Pin
import dht
import time


dht_pin = Pin(17, Pin.IN, Pin.PULL_UP)
sensor = dht.DHT22(dht_pin)

def test_dht11():
  try:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
  except Exception as e:
    print("Error reading from DHT11:", e)

while True:
    test_dht11()
    time.sleep(5)  # Espera 5 segundos antes de leer nuevamente
