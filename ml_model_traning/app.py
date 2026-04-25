import streamlit as st
import pandas as pd
import joblib
import datetime

try:
    model = joblib.load("models/ev_demand_model.pkl")
    model_loaded = True
except FileNotFoundError:
    st.error("Model file not found. Please train the model first by running: python src/train_model.py")
    model_loaded = False
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

def prediction(vehicle_model, battery_capacity, location,
               duration, charging_rate, temperature,
               vehicle_age, charger_type, user_type,
               soc_start, soc_end):

    if not model_loaded:
        st.error("Model is not loaded. Cannot make predictions.")
        return None

    # Input validation
    if soc_end <= soc_start:
        st.error("End State of Charge must be greater than Start State of Charge")
        return None

    if battery_capacity <= 0:
        st.error("Battery capacity must be greater than 0")
        return None

    if duration <= 0:
        st.error("Charging duration must be greater than 0")
        return None

    if charging_rate <= 0:
        st.error("Charging rate must be greater than 0")
        return None

    soc_change = soc_end - soc_start

    now = datetime.datetime.now()
    hour = now.hour
    month = now.month
    day_of_week = now.weekday()
    is_weekend = 1 if day_of_week >= 5 else 0

    input_df = pd.DataFrame([{
        "Vehicle Model": vehicle_model,
        "Battery Capacity (kWh)": battery_capacity,
        "Charging Station Location": location,
        "Charging Duration (hours)": duration,
        "Charging Rate (kW)": charging_rate,
        "Temperature (°C)": temperature,
        "Vehicle Age (years)": vehicle_age,
        "Charger Type": charger_type,
        "User Type": user_type,
        "soc_change": soc_change,
        "hour": hour,
        "month": month,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend
    }])

    return model.predict(input_df)[0]

def main():
    st.title("EV Charging Demand Predictor")
    st.header("Enter Charging Session Details")

    vehicle_model = st.selectbox("Vehicle Model",
        ("Tesla Model 3", "Nissan Leaf", "BMW i3", "Hyundai Kona"))

    battery_capacity = st.number_input("Battery Capacity (kWh)", min_value=10.0)

    location = st.selectbox("Charging Station Location",
        ("New York", "Los Angeles", "Houston", "San Francisco"))

    duration = st.number_input("Charging Duration (hours)", min_value=0.1)

    charging_rate = st.number_input("Charging Rate (kW)", min_value=1.0)

    temperature = st.number_input("Temperature (°C)")

    vehicle_age = st.number_input("Vehicle Age (years)", min_value=0)

    charger_type = st.selectbox("Charger Type",
        ("Level 1", "Level 2", "DC Fast Charger"))

    user_type = st.selectbox("User Type",
        ("Commuter", "Casual Driver", "Long-Distance Traveler"))

    soc_start = st.slider("State of Charge Start (%)", 0, 100, 20)
    soc_end = st.slider("State of Charge End (%)", 0, 100, 80)

    if st.button("Predict Energy Consumption"):
        if not model_loaded:
            st.error("Cannot make predictions. Model is not loaded.")
        else:
            result = prediction(vehicle_model, battery_capacity, location,
                                duration, charging_rate, temperature,
                                vehicle_age, charger_type, user_type,
                                soc_start, soc_end)

            if result is not None:
                st.success(f"Predicted Energy Consumption: {round(result, 2)} kWh")


if __name__ == "__main__":
    main()