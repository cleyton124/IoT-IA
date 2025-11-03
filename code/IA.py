# ia_rule.py
import requests
import time

CHANNEL_ID = "3129290"
WRITE_KEY = "CJ0GUGJ5A65SATSM"
READ_KEY = "3H7SWO34AIAHRL3N" 

THRESHOLD_TEMP = 30.0  # exemplo: se temp > 30 => liga

def get_latest():
    url = f"http://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results=10"
    if READ_KEY:
        url += f"&api_key={READ_KEY}"
    r = requests.get(url, timeout=10)
    data = r.json()
    feeds = data.get("feeds", [])
    temps = []
    for f in feeds:
        v = f.get("field1")
        if v is not None:
            try:
                temps.append(float(v))
            except:
                pass
    return temps

def write_command(value):
    url = "http://api.thingspeak.com/update"
    payload = {"api_key": WRITE_KEY, "field3": value}
    r = requests.post(url, data=payload, timeout=10)
    return r.text

while True:
    temps = get_latest()
    if len(temps) == 0:
        print("Sem dados ainda.")
    else:
        avg = sum(temps)/len(temps)
        print("Temperaturas recentes média:", avg)
        if avg > THRESHOLD_TEMP:
            print("Decisão: LIGAR")
            write_command(1)
        else:
            print("Decisão: DESLIGAR")
            write_command(0)
    time.sleep(25)  # intervalo maior 
