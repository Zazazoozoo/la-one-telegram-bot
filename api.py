import requests
import aiohttp
from models import Exchange, Weather
from config import OPENWEATHERMAP_API_KEY, EXCHANGERATE_API_KEY

async def get_weather(city: str) -> Weather:
    api_key = OPENWEATHERMAP_API_KEY
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                return None
            data = await response.json()
            print(data)
            city = data['name']
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            weather_data = Weather.Weather(city, temp, description)
            return weather_data


async def get_exchange_rate(base_currency: str, target_currency: str) -> Exchange:
    api_key = EXCHANGERATE_API_KEY
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={target_currency}&from={base_currency}&amount=1"
    headers = {
        "apikey": api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()
    exchange_rate = data['result']
    # exchange_rate = Exchange.Exchange(base_currency, target_currency, exchange_rate)
    return exchange_rate