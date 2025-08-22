# Weather Chatbot api
from flask import Flask, request, jsonify
import requests
import dotenv
import flask_cors

app = Flask(__name__)

# Enable CORS for all routes
flask_cors.CORS(app)

apikey   =   dotenv.dotenv_values(".env")["apikey"]
base_url =   "http://api.openweathermap.org/data/2.5/weather"

@app.route("/weather", methods=["GET", "POST"])
def get_weather():
    # Handle POST (chatbot) or GET (browser)
    if request.method == "POST":
        data = request.get_json()
        city = data.get("city") if data else None
    else:
        city = request.args.get("city")

    if not city:
        return jsonify({"error": "Please provide a city"}), 400

    params = {"q": city, "appid": apikey, "units": "metric"}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "City not found or API error"}), 404

    data = response.json()
    result = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
        
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)