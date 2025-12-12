import requests

api_key = "e843332f60a58f2e5eff868153d40275"
city = input("Enter city= ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
print("Status= ", response.status_code)
weather = response.json()
print("Temperature= ", weather["main"]["temp"])
print("Humidity= ", weather["main"]["humidity"])
print("Wind speed= ",weather["wind"]["speed"])

