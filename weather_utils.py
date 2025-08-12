import pandas as pd

def get_recent_rainfall(region, n_months=6, csv_path="Indian Rainfall Dataset District-wise Daily Measurements.csv"):
    try:
        df = pd.read_csv(csv_path)

        # Clean and convert date
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.to_period('M')

        # Group by district and month
        monthly_avg = df.groupby(['District', 'Month'])['Rainfall'].mean().reset_index()

        # Filter by region (case-insensitive)
        region_data = monthly_avg[monthly_avg['District'].str.lower() == region.lower()]
        recent_data = region_data.sort_values(by='Month', ascending=False).head(n_months)

        # Return average rainfall for last `n_months`
        return round(recent_data['Rainfall'].mean(), 2)

    except Exception as e:
        print("Rainfall forecast error:", e)
        return None
