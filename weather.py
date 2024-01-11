import requests
from bs4 import BeautifulSoup
import re
import sys

def get_weather_forecast(zip_code):
    url = f"https://weather.com/weather/tenday/l/{zip_code}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_container = soup.find("div", class_=(re.compile("DailyForecast--DisclosureList")))

    for detail in forecast_container.find_all("details"):
        print(detail.find("div", class_=(re.compile("DetailsSummary"))).text)


if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    try:
        print(get_weather_forecast(zip_code))
    except:
        print("Error")
        sys.exit()
