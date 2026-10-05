# 3D-Cloud-Tracking-System

The **3D Cloud Tracking System** is an interactive web application that provides real-time weather and cloud coverage information using a 3D globe visualization. The system allows users to explore current weather conditions for any city and track cloud coverage on a 3D map, providing an engaging way to visualize weather data.

## Features

- **Interactive 3D Globe**: Visualizes cloud coverage, weather data, and allows users to interact with a rotating 3D globe.
- **City Search**: Users can search for a city by name to retrieve weather data and cloud coverage for that location.
- **Real-Time Weather Data**: Displays key weather details including temperature (Celsius/Fahrenheit), humidity, wind speed, and a weather description.
- **Cloud Coverage Data**: Uses OpenWeatherMap API to fetch cloud coverage percentage and overlay it on the map.
- ## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Dash (Interactive web application framework built on top of Plotly)

- **Visualization**: Plotly (3D globe visualization)
                     Pydeck(For displaying OpenStreetMap tiles with additional weather layers)
- **Database**: SQLite (for storing weather data)
- **API**: OpenWeatherMap (for fetching weather and cloud data)
- **Other Libraries**: `requests`, `datetime`, `SQLAlchemy`

## Setup Instructions
3d-cloud-tracking-system/
│
├── app.py                     # Main Python file for running the app
├── README.md                  # Project description and instructions
│
├── static/                    # Folder for static files like images, CSS, etc.
│   │   └── styles.css         # Custom CSS for the app

### Prerequisites

1. **Python 3.x** installed on your machine.
2. An account on OpenWeatherMap to generate an API key.
3. Basic knowledge of using the command line.

### Configure the API key

1. Install the dependencies with `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env`.
3. Replace the example value with your OpenWeatherMap API key.
4. Start the application with `python app.py`.

The `.env` file is ignored by Git. Do not commit API keys or share them publicly.

## Designed And Developed by-
- **Rishabh Tiwari**
- ***Contact***: +91 9452302696
- ***Email***: rishabhtiwari0019@gmail.com
- ***College***: GL Bajaj Group Of Institutions, Mathura
