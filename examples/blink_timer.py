import machine
import time

led_pin = machine.Pin(12, machine.Pin.OUT)
led_pin.off()

# Configuración del temporizador
timer = machine.Timer(0)

def toggle_led(timer):
    print("LED cambiado de estado.")
    led_pin.value(not led_pin.value())

# Configura el temporizador para llamar a toggle_led cada 1 segundo
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=toggle_led)

# Hilo principal
try:
    while True:
        time.sleep(5)
        print("Hilo principal en ejecución...")
finally:
    timer.deinit()
