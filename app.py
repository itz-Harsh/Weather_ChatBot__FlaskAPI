from flask import Flask, request, jsonify
import requests
from collections import defaultdict
import dotenv
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

API_KEY = dotenv.dotenv_values(".env")["apikey"]

CURRENT_URL  = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


@app.route("/weather", methods=["GET", "POST"])
def weather():
    # 1️⃣ Get city
    if request.method == "POST":
        payload = request.get_json(silent=True)
        city = payload.get("city") if payload else None
    else:
        city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # 2️⃣ Call CURRENT weather
    try:
        current_res = requests.get(CURRENT_URL, params=params, timeout=8)
        current_res.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Current weather timeout"}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "Current weather API error"}), 502

    current_raw = current_res.json()

    # 3️⃣ Call FORECAST
    try:
        forecast_res = requests.get(FORECAST_URL, params=params, timeout=8)
        forecast_res.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Forecast timeout"}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "Forecast API error"}), 502

    forecast_raw = forecast_res.json()

    # 4️⃣ Parse CURRENT
    current = {
        "temperature": current_raw["main"]["temp"],
        "feels_like": current_raw["main"]["feels_like"],
        "humidity": current_raw["main"]["humidity"],
        "pressure": current_raw["main"]["pressure"],
        "description": current_raw["weather"][0]["description"],
        "wind_speed": current_raw["wind"]["speed"]
    }

    # 5️⃣ Parse FORECAST (5-day daily summary)
    daily = defaultdict(list)

    for item in forecast_raw["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily[date].append(item)

    forecast = []

    for date, entries in list(daily.items())[:10]:
        temps = [e["main"]["temp"] for e in entries]

        forecast.append({
            "date": date,
            "min_temp": round(min(temps), 1),
            "max_temp": round(max(temps), 1),
            "description": entries[0]["weather"][0]["description"],
            "humidity": entries[0]["main"]["humidity"],
            "wind_speed": entries[0]["wind"]["speed"]
        })

    # 6️⃣ Final PERFECT response
    return jsonify({
        "city": current_raw["name"],
        "country": current_raw["sys"]["country"],
        "coordinates": {
            "lat": current_raw["coord"]["lat"],
            "lon": current_raw["coord"]["lon"]
        },
        "current": current,
        "forecast": forecast
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
