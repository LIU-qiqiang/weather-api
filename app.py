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
    date = data.get("date")  # 当前暂不使用日期，后续可以扩展为 forecast 接口

    if not location or not date:
        return jsonify({"error": "Please provide both 'location' and 'date'"}), 400
    encoded_location = urllib.parse.quote(location)
    # 构造 OpenWeatherMap 请求 URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_location}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        print("DEBUG URL:", url)
        print("DEBUG Response:", response.text)
        weather_data = response.json()

        if response.status_code != 200 or "weather" not in weather_data:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        weather_main = weather_data["weather"][0]["main"].lower()

        # 简单推荐逻辑
        if "rain" in weather_main:
            recommendation = "Carry an umbrella"
        elif "clear" in weather_main:
            recommendation = "Good to go"
        elif "cloud" in weather_main:
            recommendation = "Might be cloudy, check again later"
        else:
            recommendation = "Check local weather for more info"

        result = {
            "location": location,
            "date": date,
            "weather": weather_main,
            "recommendation": recommendation
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
