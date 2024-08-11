#!/usr/bin/env python
'''
Weather scraping script that extracts "ten day" weather forecasts for a given ZIP code from weather.com
Adapted to work with Flask

'''


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

__author__ = "Bao Dinh"
__version__ = "2.0.1"
__maintainer__ = "Bao Dinh"
__email__ = "baondinh@bu.edu"

def get_weather_forecast(zip_code):
    """
    Retrieves weather forecast for a given zip code from weather.com.

    Args:
        zip_code (str): 5-digit zip code.

    Returns:
        forecasts (list): A list of strings representing the weather forecast for each day.
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

def split_weather_line(forecasts):
    """
    Uses regex to extract weather data from string forecasts returned by `get_weather_forecast()`

    Args:
        forecasts (lst): A list of strings representing the weather forecast for each day.

    Returns:
        results (list): A list of dictionaries with weather information for daily forecasts.
    """

    # Weather options for use with f-string regex
    wind_direction_options = "N|NNE|NE|ENE|E|ESE|SE|SSE|S|SSW|SW|WSW|W|WNW|NW|NNW"
    condition_options = "Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow|Thunderstorms|Scattered Thunderstorms|Thunderstorms Early"

    # First split of forecast data into broader weather data categories
    date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
    wind_pattern = fr"Wind({wind_direction_options})\s{{0,1}}(\d{{1,2}})\s{{0,1}}mph"
    condition_pattern = fr"({condition_options})"
    temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"

    results = []

    # For each line in forecasts list (daily forecasts), create a dictionary of separated weather data
    for line in forecasts:
        date_match = re.search(date_pattern, line)
        condition_match = re.search(condition_pattern, line)
        temp_match = re.search(temp_pattern, line)
        wind_match = re.search(wind_pattern, line)

        # Second split of forecast data
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

def analyze_weather_data(df):
    """
    Analyzes numerical weather data and generates a line graph of high/low temperatures from a DataFrame of the weather data.

    Args:
        df (DataFrame): DataFrame created from returned list of dictionaries from `split_weather_line()`.
    """
    print("\nData Analysis:")
    print(df.describe())
    
    print("\nCorrelation Matrix:")
    correlation_matrix = df[['high_temp', 'low_temp', 'wind_speed', 'rain_chance']].corr()
    print(correlation_matrix)
    
def plot_weather_data(df):
    """
    Creates a matplotlip line graph of high and low temperatures extracted from weather data DataFrame

    Args:
        df (DataFrame): DataFrame created from returned list of dictionaries from `split_weather_line()`.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['high_temp'], label='High Temp', color='red')
    plt.plot(df['date'], df['low_temp'], label='Low Temp', color='blue')
    plt.fill_between(df['date'], df['high_temp'], df['low_temp'], alpha=0.2)
    plt.title('Temperature Range Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°F)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close(img)

    # Encode image to base64
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return plot_url

def get_weather_data(zip_code):
    """
    Makes calls to other functions to obtain weather data, parse weather data, and reformat data as a Pandas DataFrame.

    Args:
        zip_code (int): ZIP code to obtain weather data from weather.com instead of user ZIP code input.
        
    Returns:
        df (DataFrame): Reformatted weather data as a Pandas DataFrame.
    """
    try:
        forecasts = get_weather_forecast(zip_code)
        parsed_forecasts = split_weather_line(forecasts)
        
        # Create DataFrame
        df = pd.DataFrame(parsed_forecasts)
        
        # Plot data and get base64 encoded image
        # plot_url = plot_weather_data(df)
        return df
        # return df, plot_url
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
