from services.weather_services import get_weather

API_KEY = "e843332f60a58f2e5eff868153d40275"
city = input("Enter city= ")
data = get_weather(city, API_KEY)

print("Weather data for",city)
print("Temperature=",data["main"]["temp"],"°C")
print("Humidity=",data["main"]["humidity"],"%")
print("Description=",data["weather"][0]["description"])

