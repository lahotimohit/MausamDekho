import requests
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "a8a6711b6ca8fce79ffbfa20b5325f3f"


class WeatherForecast:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def weather_forecast(self):
        parameters = {
            'lat': self.latitude,
            'lon': self.longitude,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(url=BASE_URL, params=parameters)
        return response.json()
    