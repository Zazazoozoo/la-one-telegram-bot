import requests
import os
from flask import Flask, jsonify, request, Blueprint
from app.models.Weather import Weather


weather = Blueprint(
    'weather',
    __name__,
    url_prefix='/api'
)


@weather.route('/weather/<city>', methods=['GET', 'POST'])
def get_weather(city):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return response.json()
    data = response.json()

    # Map the weather data onto the Weather model
    city = data['name']
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    weather_data = Weather(city, temp, description)


    return jsonify(weather_data.__dict__)

@weather.route('/', methods=['GET', 'POST'])
def index():
    return "Hello world"