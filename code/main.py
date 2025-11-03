# main.py  (MicroPython)
import network
import time
try:
    import urequests as requests
except:
    import requests
import dht
from machine import Pin
import urandom as random 

# --- CONFIGURAÇÕES WI-FI ---
SSID = "Wokwi-GUEST"
PASSWORD = ""

# --- CONFIGURAÇÕES THINGSPEAK ---
THINGSPEAK_URL = "https://api.thingspeak.com/update"
API_KEY = "CJ0GUGJ5A65SATSM" 

# --- BUFFER PARA DETECÇÃO (anomaly) ---
BUFFER = []
BUFFER_MAX = 20  # número de leituras para estatística
MIN_READS_FOR_DETECT = 6

def push_buffer(val):
    if len(BUFFER) >= BUFFER_MAX:
        BUFFER.pop(0)
    BUFFER.append(val)

def is_anomaly(val):
    if len(BUFFER) < MIN_READS_FOR_DETECT:
        return False
    mean = sum(BUFFER) / len(BUFFER)
    var = sum((x - mean) ** 2 for x in BUFFER) / len(BUFFER)
    std = var ** 0.5
    if std == 0:
        return False
    z = (val - mean) / std
    return abs(z) > 3  # z-score > 3 => anômalo

# --- CONECTAR AO WI-FI ---
print("Conectando ao Wi-Fi...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.5)
print("\n✅ Conectado:", wlan.ifconfig())

# --- SENSOR DHT22 (ou simulação) ---
USE_SIMULATION = False  # True para gerar valores aleatórios 
sensor = dht.DHT22(Pin(15))

def read_sensor():
    if USE_SIMULATION:
        # simula temperatura entre 20 e 32 e umidade 30-80
        t = 20 + (random.getrandbits(8) % 13)  # inteiro 20..32
        h = 30 + (random.getrandbits(8) % 51)  # 30..80
        return float(t), float(h)
    else:
        sensor.measure()
        return float(sensor.temperature()), float(sensor.humidity())

def enviar_dados(temp, umid, status, predicted=None):
    try:
        url = f"{THINGSPEAK_URL}?api_key={API_KEY}&field1={temp}&field2={umid}&field3={status}"
        if predicted is not None:
            url += f"&field4={predicted}"
        r = requests.get(url)
        print(f"✅ Dados enviados: T={temp}C U={umid}% S={status} | Resp:{r.text}")
        try:
            r.close()
        except:
            pass
    except Exception as e:
        print("❌ Erro ao enviar:", e)

# --- LOOP PRINCIPAL ---
while True:
    try:
        temperatura, umidade = read_sensor()
        # atualiza buffer e detecta anomalia
        push_buffer(temperatura)
        anomaly = is_anomaly(temperatura)
        # Status = 1 se temperatura > 28°C ou umidade > 70% ou anomalia estatística
        status = 1 if (temperatura > 28 or umidade > 70 or anomaly) else 0

        print(f"🌡️ {temperatura}°C | 💧 {umidade}% | Anomalia={anomaly} | Status={status}")
        enviar_dados(temperatura, umidade, status)
    except Exception as e:
        print("Erro de leitura/enviar:", e)

    time.sleep(20)  # tempo de envio
