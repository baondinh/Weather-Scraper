#!/usr/bin/env python
'''
Weather scraping script that extracts "ten day" weather forecasts for a given ZIP code from weather.com
Combines and improves upon functions found in both `forecast_parser.py` and `weather_scraper.py`

'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt

__author__ = "Bao Dinh"
__version__ = "1.0.1"
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
        
    Returns:
        plot_filename (str): String of filename to save line plot as.
    """
    
    print("\nData Analysis:")
    print(df.describe())
    
    print("\nCorrelation Matrix:")
    correlation_matrix = df[['high_temp', 'low_temp', 'wind_speed', 'rain_chance']].corr()
    print(correlation_matrix)
    
    # Plotting temperature range with shaded area and grid
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
    
    # Save the plot as an image with dynamic filename
    plot_filename = f"temperature_plot_{zip_code}_{datetime.now().strftime('%Y%m%d')}.png"
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename

if __name__ == "__main__":
    zip_code = input("Enter 5-digit zip code: ")
    try:
        forecasts = get_weather_forecast(zip_code)
        parsed_forecasts = split_weather_line(forecasts)
        
        # Create DataFrame 
        df = pd.DataFrame(parsed_forecasts)
        
        # Display DataFrame
        print("\nWeather Forecast DataFrame:")
        print(df)
        
        # Analyze data and get plot filename
        plot_filename = analyze_weather_data(df)
        
        # Save plot and weather data as dynamic PNG and CSV files respectively
        current_date = datetime.now().strftime("%Y%m%d")
        csv_filename = f"weather_forecast_{zip_code}_{current_date}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nData saved to {csv_filename}")
        print(f"Plot saved as {plot_filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
