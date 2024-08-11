import network
import esp
esp.osdebug(None)
import gc
import config
from time import sleep

gc.collect()

def connect():
  station = network.WLAN(network.STA_IF)
  attempt = 0
  max_attempts = 25
  if not station.isconnected():
    ssid = config.ssid
    password = config.password
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected() and attempt < max_attempts:
      attempt += 1
      sleep(0.5)
    if not station.isconnected():
      print('Sense withouth internet connection')
      return
  print('IP address:', station.ifconfig()[0])

connect()
