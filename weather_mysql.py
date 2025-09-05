import requests
import os
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime

load_dotenv()
API_KEY= os.getenv("OPENWEATHER_API_KEY")

print("API Key Loaded:", API_KEY[:5], "********")

CITY = "Chennai"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()
print(data)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

latitude = data["coord"]["lat"]
longitude = data["coord"]["lon"]
dt = datetime.fromtimestamp(data["dt"])
sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
sunset = datetime.fromtimestamp(data["sys"]["sunset"])
temperature = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
humidity = data["main"]["humidity"]
uvi = 0
clouds = data["clouds"]["all"]
weather_main = data["weather"][0]["main"]
weather_description = data["weather"][0]["description"]

query = """
INSERT INTO weather_data
(city, latitude, longitude, dt, sunrise, sunset, temperature, feels_like, humidity, uvi, clouds, weather_main, weather_description)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = (CITY, latitude, longitude, dt, sunrise, sunset, temperature, feels_like, humidity, uvi, clouds, weather_main, weather_description)

try:
    cursor.execute(query, values)
    db.commit()
    print("Weather data inserted!")
except Exception as e:
    print("Insert failed:", e)
