from flask import Flask, request, jsonify
import requests
from collections import defaultdict
import os
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

API_KEY = os.environ.get("apikey")

CURRENT_URL  = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# ISO 3166-1 alpha-2 → Country name (major + commonly used)
COUNTRY_MAP = {
    "IN": "India",
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "NZ": "New Zealand",
    "DE": "Germany",
    "FR": "France",
    "IT": "Italy",
    "ES": "Spain",
    "PT": "Portugal",
    "NL": "Netherlands",
    "BE": "Belgium",
    "CH": "Switzerland",
    "AT": "Austria",
    "SE": "Sweden",
    "NO": "Norway",
    "FI": "Finland",
    "DK": "Denmark",
    "IE": "Ireland",
    "PL": "Poland",
    "CZ": "Czech Republic",
    "HU": "Hungary",
    "RO": "Romania",
    "UA": "Ukraine",
    "RU": "Russia",
    "TR": "Turkey",
    "GR": "Greece",

    "CN": "China",
    "JP": "Japan",
    "KR": "South Korea",
    "KP": "North Korea",
    "TW": "Taiwan",
    "HK": "Hong Kong",
    "SG": "Singapore",
    "MY": "Malaysia",
    "TH": "Thailand",
    "VN": "Vietnam",
    "ID": "Indonesia",
    "PH": "Philippines",
    "BD": "Bangladesh",
    "PK": "Pakistan",
    "LK": "Sri Lanka",
    "NP": "Nepal",
    "MM": "Myanmar",

    "BR": "Brazil",
    "AR": "Argentina",
    "CL": "Chile",
    "CO": "Colombia",
    "PE": "Peru",
    "VE": "Venezuela",
    "MX": "Mexico",

    "ZA": "South Africa",
    "NG": "Nigeria",
    "KE": "Kenya",
    "EG": "Egypt",
    "MA": "Morocco",
    "DZ": "Algeria",
    "GH": "Ghana",
    "ET": "Ethiopia",

    "AE": "United Arab Emirates",
    "SA": "Saudi Arabia",
    "QA": "Qatar",
    "KW": "Kuwait",
    "OM": "Oman",
    "BH": "Bahrain",
    "IL": "Israel",
    "IR": "Iran",
    "IQ": "Iraq",
    "JO": "Jordan",

    "IS": "Iceland",
    "RS": "Serbia",
    "SK": "Slovakia",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "SI": "Slovenia",
    "LT": "Lithuania",
    "LV": "Latvia",
    "EE": "Estonia",

    "CU": "Cuba",
    "DO": "Dominican Republic",
    "JM": "Jamaica"
}


@app.route("/weather", methods=["GET", "POST"])
def weather():
    # Get city
    if request.method == "POST":
        payload = request.get_json(silent=True)
        city = payload.get("city") if payload else None
    else:
        city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    if not API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # Current weather
    try:
        current_res = requests.get(CURRENT_URL, params=params, timeout=8)
        current_res.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Current weather timeout"}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "Current weather API error"}), 502

    current_raw = current_res.json()

    # Forecast
    try:
        forecast_res = requests.get(FORECAST_URL, params=params, timeout=8)
        forecast_res.raise_for_status()
    except requests.exceptions.Timeout:
        return jsonify({"error": "Forecast timeout"}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": "Forecast API error"}), 502

    forecast_raw = forecast_res.json()

    # Parse current
    current = {
        "temperature": current_raw["main"]["temp"],
        "feels_like": current_raw["main"]["feels_like"],
        "humidity": current_raw["main"]["humidity"],
        "pressure": current_raw["main"]["pressure"],
        "description": current_raw["weather"][0]["description"],
        "wind_speed": current_raw["wind"]["speed"]
    }

    # Parse forecast (daily summary)
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

    country_code = current_raw["sys"]["country"]
    country_name = COUNTRY_MAP.get(country_code, country_code)

    return jsonify({
        "city": current_raw["name"],
        "country": country_name,
        "country_code": country_code,
        "coordinates": {
            "lat": current_raw["coord"]["lat"],
            "lon": current_raw["coord"]["lon"]
        },
        "current": current,
        "forecast": forecast
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
