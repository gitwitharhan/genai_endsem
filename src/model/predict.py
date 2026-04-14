import joblib

model = joblib.load("../models/ev_demand_model.pkl")

def predict_batch(df):
    return model.predict(df)