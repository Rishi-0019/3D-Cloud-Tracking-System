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
- **Database**: SQLite (for storing weather data)
- **API**: OpenWeatherMap (for fetching weather and cloud data)
- **Other Libraries**: `requests`, `datetime`, `SQLAlchemy`

## Setup Instructions

### Prerequisites

1. **Python 3.x** installed on your machine.
2. Basic knowledge of using the command line.
