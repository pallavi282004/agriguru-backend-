import pandas as pd
import os
import pickle
import numpy as np
from xgboost import XGBClassifier, XGBRegressor
from sqlalchemy import create_engine
from weather_utils import get_recent_rainfall
from sklearn.preprocessing import LabelEncoder
from twilio.rest import Client

# Load crop data directly from CSV
df = pd.read_csv("crop_data.csv")

# Label encode the target column
le = LabelEncoder()
df['CropLabel'] = le.fit_transform(df['best_crop'])

# Generate dummy yield values
df['Yield'] = np.random.uniform(1.5, 3.5, size=len(df))

# Train models
xgb_crop = XGBClassifier(eval_metric="mlogloss")
xgb_crop.fit(df[['rainfall', 'temperature']], df['CropLabel'])

xgb_yield = XGBRegressor()
xgb_yield.fit(df[['rainfall', 'temperature']], df['Yield'])

# Crop Recommendation
def recommend_crop(soil, rainfall, temperature, region):
    key = f"{soil}_{rainfall}_{temperature}_{region}"
    if cached := load_cache(key):
        return cached
    prediction = xgb_crop.predict([[rainfall, temperature]])
    crop = le.inverse_transform(prediction)[0]
    cache_result(key, crop)
    return crop

# Load the trained yield model
with open("yield_model.pkl", "rb") as f:
    model = pickle.load(f)

# Yield Prediction
def predict_yield(rainfall, temperature, ph, area):
    input_data = pd.DataFrame([{
        "rainfall": rainfall,
        "temperature": temperature,
        "pH": ph,
        "area": area
    }])
    prediction = model.predict(input_data)
    return round(float(prediction[0]), 2)


# Market Price Estimation (dummy logic)
def estimate_price(crop, region):
    dummy_prices = {"Rice": 20, "Wheat": 22, "Millet": 18}
    return dummy_prices.get(crop, 25)

# Multilingual Translation (simulated)
translations = {
    "Rice": {"hi": "चावल", "ta": "அரிசி"},
    "Wheat": {"hi": "गेहूं", "ta": "கோதுமை"},
    "Millet": {"hi": "बाजरा", "ta": "கம்பு"}
}

def translate_crop(crop, lang):
    return translations.get(crop, {}).get(lang, crop)

# Twilio Voice Call Alert (credentials required)
def send_voice_alert(message, to_number, lang='en'):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    language_map = {
        'en': ('en-US', 'alice'),
        'hi': ('hi-IN', 'alice'),
        'te': ('te-IN', 'alice'),
    }

    lang_code, voice_name = language_map.get(lang, ('en-US', 'alice'))

    twiml = f'''
        <Response>
            <Say language="{lang_code}" voice="{voice_name}">{message}</Say>
        </Response>
    '''

    call = client.calls.create(
        twiml=twiml,
        to=to_number,
        from_='+13185923753'
    )

    return call.sid

# Offline Caching using Pickle
CACHE_FILE = "crop_cache.pkl"

def cache_result(key, value):
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
    cache[key] = value
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)

def load_cache(key):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
            return cache.get(key)
    return None
