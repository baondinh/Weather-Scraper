import requests
from bs4 import BeautifulSoup
import re

def split_weather_line(forecasts):
    """
    Splits weather forecast lines into their components.

    Args:
        forecasts (list): List of strings representing weather forecast lines to split.

    Returns:
        list: A list containing dictionaries of the date, condition, temperature, wind direction, and wind speed parsed from each forecast.
    """
    lst = []
    for line in forecasts:
        # Regular expressions for each component
        date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
        wind_direction_options = "N|NNE|NE|ENE|E|ESE|SE|SSE|S|SSW|SW|WSW|W|WNW|NW|NNW"
        wind_pattern = fr"Wind({wind_direction_options})\s{{0,1}}(\d{{1,2}})\s{{0,1}}mph"
        condition_options = "Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow|Thunderstorms|Scattered Thunderstorms|Thunderstorms Early"
        condition_pattern = fr"({condition_options})"
        temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"

        # Extract components
        date_match = re.search(date_pattern, line)
        condition_match = re.search(condition_pattern, line)
        temp_match = re.search(temp_pattern, line)
        wind_match = re.search(wind_pattern, line)

        dct = {}
        if date_match and condition_match and temp_match and wind_match:
            dct["date"] = date_match.group(0)
            dct["condition"] = condition_match.group(0)
            dct["temp"] = temp_match.group(0)
            dct["wind"] = f"{wind_match.group(1)} {wind_match.group(2)} mph"
            lst.append(dct)
    return lst

def get_weather_forecast(zip_code):
    """
    Retrieves weather forecast for a given zip code from weather.com.

    Args:
        zip_code (str): 5-digit zip code.

    Returns:
        list: A list of strings representing the weather forecast for each day.
    """
    url = f"https://weather.com/weather/tenday/l/{zip_code}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_container = soup.find("div", class_=(re.compile("DailyForecast--DisclosureList")))

    forecasts = []
    for detail in forecast_container.find_all("details"):
        forecast_text = detail.find("div", class_=(re.compile("DetailsSummary"))).text
        forecasts.append(forecast_text)
    return forecasts

if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    try:
        forecasts = get_weather_forecast(zip_code)
        parsed_forecasts = split_weather_line(forecasts)
        for forecast in parsed_forecasts:
            print(forecast)
    except Exception as e:
        print(f"Error: {str(e)}")
