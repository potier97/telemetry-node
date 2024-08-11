import machine
import time

led = machine.Pin(12, machine.Pin.OUT)
print("Hola, ESP32!")

while True:
    led.value(not led.value())
    time.sleep(2)