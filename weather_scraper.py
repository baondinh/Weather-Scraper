import requests
from bs4 import BeautifulSoup
import re
import sys
import forecast_parser as fp
from datetime import datetime

def get_weather_forecast(zip_code):
    url = f"https://weather.com/weather/tenday/l/{zip_code}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_container = soup.find("div", class_=(re.compile("DailyForecast--DisclosureList")))

    lst = []
    for detail in forecast_container.find_all("details"):
        lst.append(detail.find("div", class_=(re.compile("DetailsSummary"))).get_text(strip=True))

    return lst

if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    today = datetime.now() # current date and time
    try:
        forecasts = get_weather_forecast(zip_code)

        # Append parsed forecast data to a list
        parsed_list = []
        for forecast in forecasts: 
            parsed_data = fp.split_weather_line(forecast)
            parsed_list.append(parsed_data)

        #Store data in a custom CSV file
        file_name = f"weather_{zip_code}_{today.strftime("%m%d%Y")}.csv"
        fp.write_weather_csv(parsed_list, file_name)
        print(f"Forecast data stored to {file_name}")
    except:
        print("Error")
        sys.exit()
