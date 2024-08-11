import machine
import time

# Configuración del GPIO del LED
led_pin = machine.Pin(12, machine.Pin.OUT)
led_pin.off()

# Intervalo de sueño en segundos
sleep_interval = 10

def deep_sleep():
    print("El ESP está en modo de suspensión profunda.")
    machine.deepsleep(sleep_interval * 1000)

# Ejecutar una tarea antes de dormir
def main_task():
  print("Ejecutando tarea principal.")
  led_pin.on()
  time.sleep(2)
  led_pin.off()
  print("Tarea principal completada.")

main_task()
deep_sleep()
