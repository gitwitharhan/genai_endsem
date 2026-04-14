def summarize(df):
    total = df["predicted_energy"].sum()
    peak = df.groupby("hour")["predicted_energy"].sum().idxmax()

    chargers = int(total / 200)

    return {
        "total_daily_demand": round(total, 2),
        "peak_hour": int(peak),
        "chargers_needed": chargers
    }