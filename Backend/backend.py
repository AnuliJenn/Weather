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
