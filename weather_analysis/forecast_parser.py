import re
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

"""
    Splits a weather forecast line into components using regex.
    Returns a dictionary with the parsed date, condition, temperature, and wind information from each forecast line
    Or None if the line format is not recognized.
    """
def split_weather_line(day_forecast):
    lst = []
    for line in lines:
        # Regular expressions for each component
        date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
        condition_pattern = r"(Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow)"
        temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"
        wind_pattern = r"(?<=Wind)(\w{1,3}\d{1,2})mph"

        # Extract components
        try:
            date_match = re.search(date_pattern, day_forecast)
            condition_match = re.search(condition_pattern, day_forecast)
            temp_match = re.search(temp_pattern, day_forecast)
            wind_match = re.search(wind_pattern, day_forecast)
    
            dct = {}
            dct["date"] = date_match.group(0) if date_match != None else None
            dct["condition"] = condition_match.group(0) if condition_match != None else None
            dct["temp"] = temp_match.group(0) if temp_match != None else None
            dct["wind"] = wind_match.group(0) if wind_match != None else None
          
        except:
            print("Error: split_weather_line()")
            sys.exit()
    return dct

"""  
    Writes parsed weather data to a CSV file
    Writes weather data to a CSV file with separate temp columns
    """
def write_weather_csv(weather_data, file_name):  
    with open(file_name, 'w') as f:
        f.write('date,condition,high_temp,low_temp,wind\n') # Header row
        for day in weather_data:
            high, low = day["temp"].split('/')
            f.write(
                f'{day["date"]},{day["condition"]},{high},{low},'
                f'{day["wind"]}\n'
            )

"""  
    Generates matplotlib plots of temperature data stored in CSV file created with write_weather_csv()
    """
def generate_weather_plot(csv_file):
    highs = []
    lows = []
    dates = []

    # Open CSV and extract temperature data
    with open(csv_file, 'rb') as f:
        lines = f.readlines()
        reader = csv.reader([line.decode('utf-8', 'ignore') for line in lines])
        next(reader)
        
        for row in reader:
            dates.append(row[0])
            try:
                highs.append(int(row[2]))
                lows.append(int(row[3]))
            except ValueError:
                highs.append(None)
                lows.append(None)

    # Generate line graphs for temperature data and show plot        
    plt.plot(dates, highs, color='red')
    plt.plot(dates, lows, color='blue')
    plt.plot(dates, highs, 'o', color='red', label='High') 
    plt.plot(dates, lows, 'o', color='blue', label='Low')
    plt.legend()
    plt.ylim(0, 100)
    plt.yticks(np.arange(0, 100, 10))
    plt.ylabel('Temperature (°F)')
    plt.title('Daily High and Low Temperatures')
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.fill_between(dates, highs, lows, 
                    facecolor='plum', alpha=0.5)

    offset = 5
    for i in range(len(dates)): 
        plt.annotate(f"{highs[i]}°", xy = (dates[i],highs[i] + offset))
        plt.annotate(f"{lows[i]}°", xy = (dates[i],lows[i] - offset))

    plt.show()
    print('Graph generated with temperature axes fixes!')

