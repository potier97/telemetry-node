from machine import SPI, Pin
from time import sleep
import sdcard
import os

sd_spi = SPI(1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5, Pin.OUT)
sd = sdcard.SDCard(sd_spi, cs)
os.mount(sd, "/sd")

def test_sd_card():
    try:
        with open("/sd/test.txt", "w") as f:
            f.write("SD card test - Writing data\n")
        with open("/sd/test.txt", "r") as f:
            data = f.read()
            print("Read from SD:", data)
    except Exception as e:
        print("Error with SD card:", e)


while True:
    test_sd_card()
    sleep(5)
