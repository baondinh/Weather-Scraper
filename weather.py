import requests
from bs4 import BeautifulSoup
import re
import sys


"""Splits weather forecast lines into their components.

    Args:
        forecast: List of weather forecast lines to split.

    Returns:
        A list containing dictionaries of the date, condition, temperature, wind direction, and wind speed parsed from each forecast.
        Or None if the line format is not recognized.
    """
def split_weather_line(forecast):
    lst = []
    for line in lines:
        # Regular expressions for each component
        date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
        wind_pattern = r"(?<=Wind)(\w{1,3}\d{1,2})mph" # Match "Wind", 1-3 letter direction, 1-2 digit speed
        condition_pattern = r"(Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow)"
        temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"

        # Extract components
        try:
            date_match = re.search(date_pattern, line).group(0)
            condition_match = re.search(condition_pattern, line).group(0)
            temp_match = re.search(temp_pattern, line).group(0)
            wind_match = re.search(wind_pattern, line).group(0)
    
            dct = {}
            if date_match and condition_match and temp_match and wind_match: 
                dct["date"] = date_match
                dct["condition"] = condition_match
                dct["temp"] = temp_match
                dct["wind"] = wind_match
            lst.append(dct)
        except:
            print("Error: split_weather_line()")
            sys.exit()
    return lst

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
        forecast = get_weather_forecast(zip_code)
    except:
        print("Error")
        sys.exit()
