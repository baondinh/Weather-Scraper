import requests
from bs4 import BeautifulSoup
import re

def get_weather_forecast(zip_code):
    url = f"https://weather.com/weather/tenday/l/{zip_code}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_container = soup.find("div", class_=(re.compile("DailyForecast--DisclosureList")))
   
    return forecast_container

if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    print(get_weather_forecast(zip_code))
