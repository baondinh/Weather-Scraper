import requests
from bs4 import BeautifulSoup

def get_weather_forecast(zip_code):
    url = f"https://weather.com/weather/tenday/l/{zip_code}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_container = soup.find("div", class_=("DailyForecast--DisclosureList"))
    if not forecast_container:
        return None

if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    print(get_weather_forecast(zip_code))
