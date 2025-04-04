# 🌤️ 10-Day Weather Forecast Scraper & Analyzer

This project combines weather data retrieval, parsing, and visualization into a single tool. Using the bs4 library, it scrapes 10-day weather forecasts from weather.com based on a U.S. ZIP code, parses the data using regular expressions, organizes the data with pandas, and visualizes temperature trends with matplotlib.

Key Features:

- Web Scraping: Uses requests and BeautifulSoup to scrape 10-day forecast data from weather.com.
- Regex Parsing: Extracts relevant forecast details (temperature, wind, conditions, etc.) using regular expressions for flexible and robust pattern matching.
- Data Analysis with Pandas: Converts raw forecast data into a DataFrame for easy exploration and statistical analysis.
- Data Visualization with Matplotlib: Generates a temperature range plot showing high/low temps over time, saved as a .png image.
- Validation & Error Handling: Includes ZIP code format validation and error logging for robust runtime behavior.
- CSV Export: Saves cleaned and structured weather data to a dynamically named .csv file for reuse.

File Outputs: 
- weather_forecast_[ZIP_CODE]_[DATE].csv --> Summarized data from pandas DataFrame
- temperature_plot_[ZIP_CODE]_[DATE].png --> Line graph showing high and low temperatures with shaded range of temperatures for the 10 days

Example Visualization: 
![Alt text](sampleweatherplot.png?raw=true "Sample Temperature")

Further Ideas to Explore: 
- Visualization using Tableau
- Further data analysis with numpy and pandas
- API implementation
- Energy analysis for certain weather patterns
- Using CSV file with other applications like Tableau
