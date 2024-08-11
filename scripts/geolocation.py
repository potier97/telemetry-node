import urequests
import time
import config

class GeoLocation:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}"
        self.headers = {'Content-Type': 'application/json'}
        self.location = None

    def update_location(self):
        """Actualiza la ubicación geográfica basada en la IP."""
        body = {"considerIp": True}
        response = urequests.post(self.url, headers=self.headers, json=body)

        if response.status_code == 200:
            self.location = response.json()
            # print("Latitud:", self.location['location']['lat'])
            # print("Longitud:", self.location['location']['lng'])
            # print("Precisión:", self.location['accuracy'], "metros")
        else:
            print("Error en la solicitud:", response.status_code, response.text)

        response.close()

    def get_coordinates(self):
        """Devuelve la latitud y longitud actuales."""
        if self.location:
            return self.location['location']['lat'], self.location['location']['lng']
        else:
            print("Ubicación no actualizada.")
            return None, None

    def get_accuracy(self):
        """Devuelve la precisión actual de la ubicación."""
        if self.location:
            return self.location['accuracy']
        else:
            print("Ubicación no actualizada.")
            return None
