from machine import SPI, Pin
import sdcard
import os

class SDCard:
  def __init__(self, spi_sck, spi_mosi, spi_miso, cs_pin):
    self.spi = SPI(1, sck=Pin(spi_sck), mosi=Pin(spi_mosi), miso=Pin(spi_miso))
    self.cs = Pin(cs_pin, Pin.OUT)
    self.sd = sdcard.SDCard(self.spi, self.cs)
    os.mount(self.sd, "/sd")

  def write(self, file_name, data):
    """Test writing and reading from the SD card."""
    try:
      with open(f"/sd/{file_name}", "a") as f:
        f.write(data + "\n")
    except Exception as e:
      print("Error with SD card:", e)
