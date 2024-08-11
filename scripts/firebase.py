import urequests
import json

class FirebaseManager:
  def __init__(self, api_key, email, password, database_url):
    self.api_key = api_key
    self.email = email
    self.password = password
    self.database_url = database_url

  def authenticate(self):
    """Authenticate with Firebase and return the token."""
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + self.api_key
    payload = json.dumps({"email": self.email, "password": self.password, "returnSecureToken": True})
    headers = {"Content-Type": "application/json"}
    try:
      response = urequests.post(url, data=payload, headers=headers)
      result = response.json()
      if "idToken" in result:
        # print("Firebase authentication successful, Token:", result["idToken"])
        return result["idToken"]
      else:
        print("Firebase authentication failed:", result)
        return None
    except Exception as e:
      print("Error during Firebase authentication:", e)
      return None

  def send_data(self, token, node_name, data):
    """Send data to Firebase."""
    url = "{}/nodes/{}.json?auth={}".format(self.database_url, node_name, token)
    headers = {"Content-Type": "application/json"}
    try:
      response = urequests.put(url, data=json.dumps(data), headers=headers)
      if not response.status_code == 200:
        print("Failed to send data:", response.text)
    except Exception as e:
      print("Error sending data to Firebase:", e)
