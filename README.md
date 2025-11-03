# 🌡️ Projeto IoT com Raspberry Pi e ThingSpeak

Este projeto demonstra como **enviar dados de temperatura e umidade** do sensor **DHT22** (ou simulado) para o **ThingSpeak**, utilizando um **Raspberry Pi no simulador Wokwi** e **MicroPython**.

Ele também implementa uma **detecção simples de anomalias** (valores fora do padrão) usando estatística básica, tornando o sistema mais inteligente e capaz de identificar leituras atípicas.

---

## 🚀 Tecnologias Utilizadas

- 🧠 **MicroPython**
- 💻 **Raspberry Pi Pico (simulado no Wokwi)**
- 🌐 **ThingSpeak (Dashboard IoT)**
- 📶 **Wi-Fi (rede Wokwi-GUEST)**
- 🌡️ **Sensor DHT22 (real ou simulado)**

---


---

## ⚙️ Funcionalidades

✅ Conexão automática com Wi-Fi (Wokwi-GUEST)  
✅ Leitura de temperatura e umidade (sensor DHT22 ou simulado)  
✅ Envio dos dados ao **ThingSpeak** via API HTTP  
✅ Detecção de **anomalias** com base em estatística (z-score > 3)  
✅ Indicação de **status** conforme condições ambientais  
✅ Impressão dos resultados no console  

---

## 🧩 Lógica do Código

O script executa um ciclo contínuo com os seguintes passos:

1. Conecta à rede Wi-Fi configurada (`SSID` e `PASSWORD`).
2. Lê dados de temperatura e umidade do sensor DHT22.
3. Adiciona o valor de temperatura a um **buffer de histórico**.
4. Calcula média e desvio padrão das últimas leituras.
5. Detecta **anomalias** (valores que se desviam muito da média).
6. Define o `status`:
   - `1` → se temperatura > 28°C, umidade > 70% ou leitura anômala  
   - `0` → caso contrário
7. Envia os dados ao **ThingSpeak** com os seguintes campos:
   - `field1` → Temperatura (°C)
   - `field2` → Umidade (%)
   - `field3` → Status (0 ou 1)
   - `field4` → (opcional) Previsão futura
8. Aguarda **20 segundos** e repete o processo.

---

## 📡 Configurações

### 🔑 Wi-Fi
```python
SSID = "Wokwi-GUEST"
PASSWORD = ""


