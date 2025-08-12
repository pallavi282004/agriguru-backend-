from flask import Flask, request, jsonify


from agriguru_ml import (
    recommend_crop,
    predict_yield,
    estimate_price,
    translate_crop,
    send_voice_alert
)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Add database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agriguru.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example DB model to test
class CropData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))
    yield_value = db.Column(db.Float)

with app.app_context():
    db.create_all()



@app.route('/', methods=['GET'])
def home():
    return '''
        <h2> AgriGuru API is running!</h2>
        <p>Use the following POST endpoints:</p>
        <ul>
            <li><code>/api/recommend</code> – Crop Recommendation</li>
            <li><code>/api/yield</code> – Yield Prediction</li>
            <li><code>/api/price</code> – Market Price Estimation</li>
            <li><code>/send_voice_alert</code> – Twilio Voice Alert</li>
        </ul>
        <p>Send JSON data using Postman or a frontend app.</p>
    '''

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    soil = data.get("soil")
    rainfall = data.get("rainfall")
    temperature = data.get("temperature")
    region = data.get("region")

    if not all([soil, rainfall, temperature, region]):
        return jsonify({"error": "Missing required fields"}), 400

    crop = recommend_crop(soil, rainfall, temperature, region)
    return jsonify({"recommended_crop": crop})

@app.route("/api/yield", methods=["POST"])
def yield_prediction():
    data = request.json

    # Extract exactly what the model expects
    rainfall = data.get("rainfall")
    temperature = data.get("temperature")
    ph = data.get("ph")
    area = data.get("area")

    if not all([rainfall, temperature, ph, area]):
        return jsonify({"error": "Missing required fields"}), 400

    yield_value = predict_yield(rainfall, temperature, ph, area)
    return jsonify({"predicted_yield": yield_value})


@app.route("/api/price", methods=["POST"])
def price_prediction():
    data = request.json
    crop = data.get("crop")
    region = data.get("region")

    if not all([crop, region]):
        return jsonify({"error": "Missing required fields"}), 400

    price = estimate_price(crop, region)
    return jsonify({"estimated_price": price})

@app.route("/api/insights", methods=["POST"])
def market_insights():
    data = request.json
    crop = data.get("crop")
    rainfall = data.get("rainfall")
    temperature = data.get("temperature")
    ph = data.get("ph")
    area = data.get("area")
    region = data.get("region")

    if not all([crop, rainfall, temperature, ph, area, region]):
        return jsonify({"error": "Missing required fields"}), 400

    yield_val = predict_yield(rainfall, temperature, ph, area)
    price = estimate_price(crop, region)
    profit = yield_val * price

    return jsonify({
        "crop": crop,
        "region": region,
        "predicted_yield": yield_val,
        "estimated_price": price,
        "estimated_profit": round(profit, 2)
    })


@app.route("/send_voice_alert", methods=["POST"])
def voice_alert():
    data = request.json
    message = data.get("message")
    to = data.get("to")
    lang = data.get("lang", "en")  # default to English

    if not all([message, to]):
        return jsonify({"error": "Missing message or recipient number"}), 400

    try:
        sid = send_voice_alert(message, to, lang)
        return jsonify({"call_sid": sid, "status": "success"})
    except Exception as e:
        return jsonify({"message": str(e), "status": "error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
