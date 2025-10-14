Perfect project idea ✅ — this is a great small-scale IoT system:

- **ESP (Arduino)** → sends data (temperature, humidity, node ID)
    
- **FastAPI backend** → receives + stores + serves data
    
- **Streamlit frontend** → displays live readings (node 1, node 2, etc.)
    

Below is a **complete, working minimal example** — modular and ready to scale.

---

## 🧩 1. Backend – FastAPI (Python)

Save as `backend.py`

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict
import time

app = FastAPI()

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, make specific later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory data store
sensor_data: Dict[str, Dict] = {}

@app.post("/update")
async def update_data(request: Request):
    data = await request.json()
    node_id = data.get("node_id")
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if not node_id or temperature is None or humidity is None:
        return {"status": "error", "message": "Invalid data"}

    sensor_data[node_id] = {
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return {"status": "success", "node": node_id}

@app.get("/data")
def get_data():
    return sensor_data


if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
```

✅ Run backend:

```bash
python backend.py
```

Now the backend will be available at `http://localhost:8000`.

---

## 🌐 2. Frontend – Streamlit

Save as `frontend.py`

```python
import streamlit as st
import requests
import time

BACKEND_URL = "http://localhost:8000/data"

st.set_page_config(page_title="ESP Sensor Dashboard", layout="wide")
st.title("🌡️ IoT Dashboard: Temperature & Humidity")

placeholder = st.empty()

while True:
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            data = response.json()
        else:
            data = {}

        with placeholder.container():
            st.subheader("📡 Connected Nodes")
            if not data:
                st.info("Waiting for ESP nodes to send data...")
            else:
                cols = st.columns(len(data))
                for i, (node_id, node_data) in enumerate(data.items()):
                    with cols[i]:
                        st.markdown(f"### Node {node_id}")
                        st.metric("Temperature (°C)", f"{node_data['temperature']:.2f}")
                        st.metric("Humidity (%)", f"{node_data['humidity']:.2f}")
                        st.caption(f"Last update: {node_data['timestamp']}")
        time.sleep(5)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        time.sleep(5)
```

✅ Run frontend:

```bash
streamlit run frontend.py
```

Open browser → [http://localhost:8501](http://localhost:8501/)

---

## ⚙️ 3. ESP / Arduino Code (ESP8266 or ESP32)

Below is code for **ESP8266** using **DHT11 or DHT22 sensor**.

### Arduino Sketch

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

#define DHTPIN D4       // GPIO2 for DHT
#define DHTTYPE DHT11   // or DHT22
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverName = "http://<YOUR_PC_IP>:8000/update";  // Replace <YOUR_PC_IP>

const char* node_id = "1"; // Change for each ESP node (e.g., "2", "3")

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  dht.begin();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();

    if (isnan(temp) || isnan(hum)) {
      Serial.println("Failed to read from DHT sensor!");
      delay(2000);
      return;
    }

    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"node_id\": \"" + String(node_id) + "\", \"temperature\": " + String(temp) + ", \"humidity\": " + String(hum) + "}";
    
    int httpResponseCode = http.POST(jsonData);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("WiFi disconnected");
  }

  delay(5000); // send every 5s
}
```

🔹 Replace:

- `YOUR_WIFI_SSID`
    
- `YOUR_WIFI_PASSWORD`
    
- `<YOUR_PC_IP>` with your backend server’s IP address (e.g. `192.168.1.10`).
    

---

## 🧠 How It Works

1. ESP sends JSON via HTTP POST to `/update`.
    
2. FastAPI stores the latest readings per node.
    
3. Streamlit polls `/data` every 5 seconds and updates UI.
    
4. You can add more nodes — just change `node_id` in each ESP.
    

---

## 🚀 Optional Enhancements

- Add database (SQLite/PostgreSQL) in backend.
    
- Add WebSocket for live updates.
    
- Show charts (Plotly/Altair) for temp/humidity history.
    
- Add authentication.
    

---

Would you like me to extend this setup to include **data history and charts** (using SQLite + Plotly in Streamlit)? It’ll make it look more like a real IoT dashboard.

Perfect 👍 — you can easily test your **FastAPI backend** without needing the ESP yet, using a simple `curl` command or Python `requests`.

Here are a few **ready-to-run examples** you can paste in your terminal 👇

---

### 🧪 Using `curl`

Send mock temperature/humidity data to your FastAPI endpoint:

```bash
curl -X POST http://localhost:8000/update \
-H "Content-Type: application/json" \
-d '{"node_id": "1", "temperature": 26.5, "humidity": 58.2}'
```

✅ Expected JSON response:

```json
{"status":"success","node":"1"}
```

You can repeat with different node IDs to simulate multiple sensors:

```bash
curl -X POST http://localhost:8000/update \
-H "Content-Type: application/json" \
-d '{"node_id": "2", "temperature": 30.1, "humidity": 49.7}'
```

---

### 🌐 Verify the Data

Check what’s stored in the backend:

```bash
curl http://localhost:8000/data
```

✅ Expected output:

```json
{
  "1": {"temperature": 26.5, "humidity": 58.2, "timestamp": "2025-10-14 18:22:00"},
  "2": {"temperature": 30.1, "humidity": 49.7, "timestamp": "2025-10-14 18:23:00"}
}
```

---

### 🐍 Optional: Using Python (if you prefer)

You can also send data using Python:

```python
import requests

url = "http://localhost:8000/update"
data = {"node_id": "1", "temperature": 25.4, "humidity": 61.2}

r = requests.post(url, json=data)
print(r.status_code, r.json())
```

---

Would you like me to show a small **bash script** to simulate multiple nodes pushing random data automatically (useful for testing the Streamlit UI before real ESPs are connected)?