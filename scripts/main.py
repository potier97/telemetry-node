from node import SensorNode
from time import sleep
from machine import reset
import config

if __name__ == '__main__':
  try:
    sleep_time = config.sleep_time
    sensor_name = config.sensor_name
    led = 12
    node = SensorNode(sensor_name, led, sleep_time)
    node.run()
  except Exception as e:
    print("Error en el ciclo de ejecución:", e)
    reset()