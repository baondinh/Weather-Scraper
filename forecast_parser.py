def write_weather_csv(weather_data, file_name):  
    """  
    Writes parsed weather data to a CSV file
    Writes weather data to a CSV file with separate temp columns"""
    with open(file_name, 'w') as f:
        f.write('date,condition,high_temp,low_temp,wind\n') # Header row
        for day in weather_data:
            high, low = day["temp"].split('/')
            f.write(
                f'{day["date"]},{day["condition"]},{high},{low},'
                f'{day["wind"]}\n'
            )
