import network
import time
import urequests
import time
import config



def test_wifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(config.ssid, config.password)

  max_attempts = 10
  attempt = 0

  while not wlan.isconnected() and attempt < max_attempts:
    print("Connecting to WiFi...")
    time.sleep(1)
    attempt += 1

  if wlan.isconnected():
    print("Connected to WiFi. IP:", wlan.ifconfig()[0])
  else:
    print("Failed to connect to WiFi")

test_wifi()


def get_ip_location():
  url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={config.api_key}"

  headers = {
    'Content-Type': 'application/json'
  }
  
  body = {
    "considerIp": True
  }

  response = urequests.post(url, headers=headers, json=body)
  
  if response.status_code == 200:
    location = response.json()
    print("Latitud:", location['location']['lat'])
    print("Longitud:", location['location']['lng'])
    print("Precisión:", location['accuracy'], "metros")
  else:
    print("Error en la solicitud:", response.status_code, response.text)

  response.close()

# Ejecutar la función
while True:
  get_ip_location()
  print("Siguiente solicitud en 5 segundos...")
  time.sleep(5)

