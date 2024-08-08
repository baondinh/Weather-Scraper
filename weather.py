import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def split_weather_line(forecasts):
    # Patterns defined outside loop for efficiency
    wind_direction_options = "N|NNE|NE|ENE|E|ESE|SE|SSE|S|SSW|SW|WSW|W|WNW|NW|NNW"
    condition_options = "Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow|Thunderstorms|Scattered Thunderstorms|Thunderstorms Early"

    date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
    wind_pattern = fr"Wind({wind_direction_options})\s{{0,1}}(\d{{1,2}})\s{{0,1}}mph"
    condition_pattern = fr"({condition_options})"
    temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"

    results = []
    for line in forecasts:
        date_match = re.search(date_pattern, line)
        condition_match = re.search(condition_pattern, line)
        temp_match = re.search(temp_pattern, line)
        wind_match = re.search(wind_pattern, line)

        if all([date_match, condition_match, temp_match, wind_match]):
            # Temperature parsing
            temp_str = temp_match.group(0)
            if "/" in temp_str:
                high_temp, low_temp = temp_str.split("/")
                high_temp = high_temp.replace("°", "")
                low_temp = low_temp.replace("°", "")
            else:  # For cases like "--/71°"
                high_temp = "--"
                low_temp = temp_str.split("/")[1].replace("°", "")

            # Wind parsing
            wind_direction = wind_match.group(1)
            wind_speed = int(wind_match.group(2))  

            # Rain chance parsing
            rain_match = re.search(r"Rain(\d{1,3})%", line)
            rain_chance = int(rain_match.group(1)) if rain_match else 0

            # Construct results dictionary
            weather_data = {
                "date": date_match.group(0),
                "condition": condition_match.group(0),
                "high_temp": int(high_temp) if high_temp.isdigit() else None,
                "low_temp": int(low_temp),
                "wind_direction": wind_direction,
                "wind_speed": wind_speed,
                "rain_chance": rain_chance
            }
            results.append(weather_data)

    return results

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

        df = pd.DataFrame(parsed_forecasts)

        print("\nWeather Forecast DataFrame:")
        print(df)

        # Save to CSV
        csv_filename = f"weather_forecast_{zip_code}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nData saved to {csv_filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
