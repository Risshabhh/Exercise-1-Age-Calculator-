# -*- coding: utf-8 -*-
"""exercise_4_Week1_Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/103chisJWb6UdXfPPOzS-7M4_VjsBLoDV

Exercise 4
"""

# Install requests if not installed
!pip install requests

# Import libraries
import requests   # For making HTTP requests
import csv        # For writing to CSV
import os         # For checking if file exists

# Function: fetch_weather

def fetch_weather(city: str, api_key: str) -> dict:
    # Build the API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        # Make the GET request
        response = requests.get(url)
        # Check for HTTP errors
        response.raise_for_status()
        # Return the JSON response
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f" HTTP error: {http_err}")
        return {}
    except requests.exceptions.RequestException as err:
        print(f" Network error: {err}")
        return {}


# Function: analyze_weather
def analyze_weather(weather_data: dict) -> str:
    try:
        # Extract needed values
        temp = weather_data['main']['temp']
        wind_speed = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        # Temperature classification
        if temp <= 10:
            summary = "Cold (≤10°C)"
        elif temp <= 24:
            summary = "Mild (11-24°C)"
        else:
            summary = "Hot (≥25°C)"

        # Add alerts
        if wind_speed > 10:
            summary += " | High wind alert!"
        if humidity > 80:
            summary += " | Humid conditions!"
        return summary
    except KeyError:
        return "Invalid weather data!"


# Function: log_weather

def log_weather(city: str, filename: str, api_key: str):
    # Fetch data
    data = fetch_weather(city, api_key)
    if not data:
        print("Could not fetch weather data.")
        return

    # Analyze data
    summary = analyze_weather(data)

    # Prepare row
    temp = data['main']['temp']
    wind = data['wind']['speed']
    humidity = data['main']['humidity']
    row = [city, temp, wind, humidity, summary]

    # Check if file exists
    file_exists = os.path.isfile(filename)

    # Append to CSV
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if new file
            writer.writerow(["City", "Temperature (°C)", "Wind Speed (m/s)", "Humidity (%)", "Summary"])
        writer.writerow(row)

    print(f"Weather data for {city} logged to {filename}")


# usage
# Mount drive
from google.colab import drive
drive.mount('/content/drive')

# Set output file path in Drive
output_file = "/content/drive/MyDrive/weather_log.csv"

api_key = "your key"  # API key
# Call your function
log_weather("Surat", output_file, api_key)
