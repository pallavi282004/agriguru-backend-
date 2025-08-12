# AgriGuru – AI-powered Crop and Market Insights

AgriGuru is an AI-driven backend system designed to help farmers make data-backed decisions on crop selection, yield prediction, and market price estimation. It also supports multilingual voice alerts for timely agricultural advisories.

## Features
- **Crop Recommendation** – Suggests optimal crops based on soil type, rainfall, temperature, and region.
- **Yield Prediction** – Uses trained machine learning models to forecast crop yield.
- **Market Price Estimation** – Provides estimated market prices for specific crops in a region.
- **Multilingual Voice Alerts** – Sends important alerts to farmers in their preferred language.
- **Partial Offline Support** – Stores past predictions for offline reference.

## Technology Stack
- **Backend Framework:** Flask (Python)
- **Machine Learning:** XGBoost, Scikit-learn
- **Data Processing:** Pandas, NumPy
- **Database:** SQLite (local) / PostgreSQL (optional)
- **Alerts:** Twilio API
- **Testing Tools:** Thunder Client, Postman

## API Endpoints
| Method | Endpoint            | Description                   |
|--------|---------------------|-------------------------------|
| POST   | `/api/recommend`    | Returns a recommended crop    |
| POST   | `/api/yield`        | Predicts expected yield       |
| POST   | `/api/price`        | Estimates market price        |
| POST   | `/send_voice_alert` | Sends a voice alert to a user |

## Example Request
POST `/api/recommend`
```json
{
  "soil": "Loamy",
  "rainfall": 200,
  "temperature": 27,
  "region": "South"
}
#####Project Structure:
agriguru/
│── agriguru_api.py      # Flask API layer
│── agriguru_ml.py       # Machine learning logic
│── weather_utils.py     # Weather and rainfall utilities
│── yield_model.pkl      # Trained yield model file
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
How to Run Locally
Clone the repository:

git clone https://github.com/pallavi282004/agriguru-backend-.git
cd agriguru-backend-
Install dependencies:


pip install -r requirements.txt
Run the Flask server:



python agriguru_api.py
Test the API using Thunder Client or Postman at:
http://127.0.0.1:5000
Status
Backend completed and tested with Thunder Client. Ready for frontend integration.

Hackathon Context
This project was developed as part of a hackathon to provide technology-driven solutions for agriculture. The backend is built for scalability, enabling future integration with web or mobile applications.
