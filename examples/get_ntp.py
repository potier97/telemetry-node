from ntptime import settime
from time import localtime, sleep, mktime

def test_ntp_time():
    try:
        settime()
        tm = localtime()
        tm_bogota = localtime(mktime(tm) - 5*3600)
        print("Current local time:", "{}-{}-{} {}:{}:{}".format(tm_bogota[0], tm_bogota[1], tm_bogota[2], tm_bogota[3], tm_bogota[4], tm_bogota[5]))
    except Exception as e:
        print("Error getting time from NTP:", e)


while True:
    test_ntp_time()
    sleep(5)  # Wait 5 seconds before reading again

