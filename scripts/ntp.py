import time
from ntptime import settime

class NTPManager:
  @staticmethod
  def sync_time():
    """Sincroniza la hora con un servidor NTP."""
    try:
      settime()
    except Exception as e:
      print("Error al obtener la hora del servidor NTP:", e)
    
  @staticmethod
  def get_date():
    """Obtiene la fecha actual en formato DD-MM-YY."""
    try:
      tm = time.localtime()
      tm_bogota = time.localtime(time.mktime(tm) - 5*3600)
      day = f"{tm_bogota[2]:02d}"
      month = f"{tm_bogota[1]:02d}"
      year = f"{tm_bogota[0] % 100:02d}" 
      return f"{day}-{month}-{year}"
    except Exception as e:
      print("Error al obtener la fecha:", e)
      return None

  @staticmethod
  def get_time():
    """Obtiene la hora actual en formato HH:MM:SS (24 horas)."""
    try:
      tm = time.localtime()
      tm_bogota = time.localtime(time.mktime(tm) - 5*3600) 
      hours = f"{tm_bogota[3]:02d}"
      minutes = f"{tm_bogota[4]:02d}"
      seconds = f"{tm_bogota[5]:02d}"
      return f"{hours}:{minutes}:{seconds}"
    except Exception as e:
      print("Error al obtener la hora:", e)
      return None
