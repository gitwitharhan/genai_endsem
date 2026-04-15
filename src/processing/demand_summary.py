def summarize(df):
    total = df["predicted_energy"].sum()
    
    # Calculate hourly profile
    hourly_df = df.groupby("hour")["predicted_energy"].sum()
    peak = hourly_df.idxmax()
    
    # Pre-calculate list of values for the chart
    hourly_profile = [float(hourly_df.get(h, 0)) for h in range(24)]

    chargers = int(total / 200)

    return {
        "total_daily_demand": round(float(total), 2),
        "peak_hour": int(peak),
        "chargers_needed": chargers,
        "hourly_profile": hourly_profile
    }