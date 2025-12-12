import requests
BASE_URL = "https://openweathermap.org/data/2.5/weather"

def get_weather(city,api_key):
    params