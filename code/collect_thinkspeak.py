# collect_thingspeak.py
import requests
import pandas as pd

CHANNEL_ID = "3129290"  
READ_API_KEY = "3H7SWO34AIAHRL3N" 
OUT_CSV = "thingspeak_history.csv"

def fetch_feeds(results=8000):
    key_part = f"&api_key={READ_API_KEY}" if READ_API_KEY else ""
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results={results}{key_part}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    feeds = data.get("feeds", [])
    rows = []
    for f in feeds:
        rows.append({
            "created_at": f.get("created_at"),
            "temp": f.get("field1"),
            "hum": f.get("field2"),
            "status": f.get("field3"),
            "predicted": f.get("field4")
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print("Saved", OUT_CSV)

if __name__ == "__main__":
    fetch_feeds()
