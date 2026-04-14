import pandas as pd
import numpy as np

def generate_sessions(location, n=200):
    np.random.seed(42)

    data = []
    for _ in range(n):
        data.append({
            "Vehicle Model": np.random.choice(["Tesla Model 3","BMW i3","Nissan Leaf","Hyundai Kona"]),
            "Battery Capacity (kWh)": np.random.choice([40, 60]),
            "Charging Station Location": location,
            "Charging Duration (hours)": np.random.uniform(0.5, 3),
            "Charging Rate (kW)": np.random.choice([7.2, 22]),
            "Temperature (°C)": np.random.uniform(20, 35),
            "Vehicle Age (years)": np.random.randint(0, 5),
            "Charger Type": np.random.choice(["Level 1", "Level 2","DC Fast Charger"]),
            "User Type": np.random.choice(["Commuter", "Casual Driver","Long-Distance Traveler"]),
            "soc_change": np.random.randint(20, 80),
            "hour": np.random.randint(0, 24),
            "month": np.random.randint(1, 13),
            "day_of_week": np.random.randint(0, 7),
            "is_weekend": np.random.randint(0, 2)
        })

    return pd.DataFrame(data)