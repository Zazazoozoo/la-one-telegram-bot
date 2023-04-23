class Weather:
    def __init__(self, city, description, temperature, humidity=None, wind_speed=None):
        self.city = city
        self.description = description
        self.wind_speed = wind_speed
        self.temperature = temperature
        self.humidity = humidity

