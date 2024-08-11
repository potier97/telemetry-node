import urequests
import json
import config
from time import sleep, localtime

def test_firebase_auth():
  firebase_api_key = config.firebase_api_key
  firebase_email = config.firebase_email
  firebase_password = config.firebase_password
  url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + firebase_api_key
  payload = json.dumps({"email": firebase_email, "password": firebase_password, "returnSecureToken": True})
  headers = {"Content-Type": "application/json"}

  try:
    response = urequests.post(url, data=payload, headers=headers)
    result = response.json()
    if "idToken" in result:
      print("Firebase authentication successful, Token:", result["idToken"])
      return result["idToken"]
    else:
      print("Firebase authentication failed:", result)
      return None
  except Exception as e:
    print("Error during Firebase authentication:", e)
    return None

def send_data_to_firebase(token, node_name, data):
  firebase_database_url = config.firebase_database_url
  url = "{}/nodes/{}.json?auth={}".format(firebase_database_url, node_name, token)
  headers = {"Content-Type": "application/json"}
  try:
    response = urequests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
      print("Data sent successfully:", data)
    else:
      print("Failed to send data:", response.text)
  except Exception as e:
    print("Error sending data to Firebase:", e)

def test_firebase_data_send():
  token = test_firebase_auth()
  if token:
    tm = localtime()
    data = {
      "temperature": "123",
      "humidity": "123",
      "uv_index": "10",
      "timestamp": "{}-{}-{} {}:{}:{}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
    }
    # Imprimir datos a enviar
    print("Data to send:", data)
    # Enviar datos a Firebase
    send_data_to_firebase(token, "test_node", data)
  else:
    print("Unable to obtain Firebase token.")


while True:
  test_firebase_data_send()
  sleep(5)
