import requests
from flask import Flask, request, jsonify
import urllib.parse
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/check-weather', methods=['POST'])
def check_weather():
    data = request.get_json()
    location = data.get("location")
    date = data.get("date")  # 当前暂不使用日期，可用于未来扩展 forecast 接口

    if not location or not date:
        return jsonify({"error": "Please provide both 'location' and 'date'"}), 400

    encoded_location = urllib.parse.quote(location)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_location}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        print("DEBUG URL:", url)
        print("DEBUG Response:", response.text)
        weather_data = response.json()

        if response.status_code != 200 or "weather" not in weather_data:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        weather_desc = weather_data["weather"][0]["description"].lower()
        temperature = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]

        # 更丰富的推荐逻辑
        if "thunderstorm" in weather_desc:
            recommendation = "Severe weather expected, stay indoors"
        elif "rain" in weather_desc or "drizzle" in weather_desc:
            recommendation = "Carry an umbrella"
        elif "snow" in weather_desc:
            recommendation = "Dress warmly and watch your step"
        elif "clear" in weather_desc and temperature >= 25:
            recommendation = "Great weather for outdoor events"
        elif "cloud" in weather_desc:
            if "overcast" in weather_desc:
                recommendation = "Looks gloomy, maybe bring a light jacket"
            elif "scattered" in weather_desc:
                recommendation = "Some clouds, but okay to go out"
            else:
                recommendation = "Might be cloudy, but should be fine"
        elif wind_speed > 10:
            recommendation = "Windy day, avoid outdoor setups"
        else:
            recommendation = "Check again later for accurate forecast"

        result = {
            "location": location,
            "date": date,
            "weather": weather_desc,
            "temperature": temperature,
            "wind_speed": wind_speed,
            "recommendation": recommendation
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
