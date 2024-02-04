import re
import sys

"""
    Splits weather forecast lines into components using regex.
    Returns a list of dictionaries with the parsed date, condition, temperature, and wind information from each forecast line
    Or None if the line format is not recognized.
    """
def split_weather_line(lines):
    lst = []
    for line in lines:
        # Regular expressions for each component
        date_pattern = r"^Today|^Tonight|^\D{3} \d{1,2}"
        condition_pattern = r"(Mostly Sunny|Sunny|Partly Cloudy|Mostly Cloudy|Scattered Showers|Few Showers|Showers|Light Rain|Rain and Snow|Rain|Snow)"
        temp_pattern = r"\d{1,3}°/\d{1,3}°|--/\d{1,3}°"
        wind_pattern = r"(?<=Wind)(\w{1,3}\d{1,2})mph"

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
