import joblib
import os

# Robust path handling: get the directory of the current script.
base_path = os.path.dirname(os.path.abspath(__file__))
# the models directory is two levels up from src/model/
model_path = os.path.join(base_path, "../../models/ev_demand_model.pkl")

model = joblib.load(model_path)

def predict_batch(df):
    return model.predict(df)
