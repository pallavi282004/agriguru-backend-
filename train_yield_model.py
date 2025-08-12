import pandas as pd
import xgboost as xgb
import pickle

# Load dataset
df = pd.read_csv("C:/Users/plvth/Downloads/crop_yield_predictions_next_6_months.csv")
df.rename(columns={
    'rainfall_mm': 'rainfall',
    'temperature_c': 'temperature',
    'ph': 'pH',
    'area_ha': 'area',
    'yield_ton_per_ha': 'yield'
}, inplace=True)


# Encode 'crop'
df['crop'] = df['crop'].astype('category').cat.codes

# Features and label
X = df[['rainfall', 'temperature', 'pH', 'area']]
y = df['yield']

# Train model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X, y)

# Save model to yield_model.pkl
with open("yield_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to yield_model.pkl")
