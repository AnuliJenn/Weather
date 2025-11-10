import requests

def send_data():
    # --- Take inputs from user ---
    node_id = input("Enter Node ID: ").strip()
    temperature = float(input("Enter Temperature (°C): "))
    humidity = float(input("Enter Humidity (%): "))

    # --- API endpoint ---
    url = "http://localhost:8000/update"

    # --- JSON payload ---
    data = {
        "node_id": node_id,
        "temperature": temperature,
        "humidity": humidity
    }

    print("\n📡 Sending data to server...")
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Successfully sent data!")
            print("Response:", response.json())
        else:
            print(f"Failed to send data. Status: {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)


if __name__ == "__main__":
    send_data()
