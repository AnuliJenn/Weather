import streamlit as st
import requests
import time

BACKEND_URL = "http://localhost:8000/data"

st.set_page_config(page_title="ESP Sensor Dashboard", layout="wide")
st.title("IoT Dashboard: Temperature & Humidity")

placeholder = st.empty()

while True:
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            data = response.json()
        else:
            data = {}

        with placeholder.container():
            st.subheader("Connected Nodes")
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
