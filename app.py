import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()


def get_api_key():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENWEATHER_API_KEY is not set. Add it to your .env file."
        )
    return api_key


# Initialize Flask app and Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Configure SQLite Database
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# Weather Data Model
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    temperature_celsius = db.Column(db.Float, nullable=False)
    temperature_fahrenheit = db.Column(db.Float, nullable=False)
    feels_like_celsius = db.Column(db.Float, nullable=False)
    feels_like_fahrenheit = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Helper function to convert from Kelvin to Celsius and Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = get_api_key()

    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None  # Return None if city is not found or there is an error in the response

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    wind_speed = response['wind']['speed']

    weather_data = {
        'city': city,
        'temperature_celsius': round(temp_celsius, 2),
        'temperature_fahrenheit': round(temp_fahrenheit, 2),
        'feels_like_celsius': round(feels_like_celsius, 2),
        'feels_like_fahrenheit': round(feels_like_fahrenheit, 2),
        'humidity': humidity,
        'wind_speed': wind_speed,
        'description': description
    }
    return weather_data

# Function to get latitude and longitude from city name
def get_lat_lon(city):
    API_KEY = get_api_key()
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'

    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'coord' in data:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None  # Handle invalid city gracefully

# Function to fetch cloud coverage data
def get_cloud_data(city):
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return None, None, None  # Return None if city coordinates are not found
    
    api_key = get_api_key()
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None, None, None  # Return None if API response is not successful
    
    data = response.json()
    clouds = data['clouds']['all']  # Cloud coverage percentage
    return clouds, lat, lon

# 3D Globe Rendering Function
def create_3d_globe(city, cloud_data, lat, lon):
    fig = go.Figure(go.Scattergeo(
        lat=[lat], lon=[lon],
        text=f"{city}\nCloud Coverage: {cloud_data}%",
        mode='markers+text',
        marker=dict(size=12, color='blue', opacity=0.7)
    ))

    # Update the projection to make it look like a 3D globe
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="white",
        lakecolor="lightblue",
    )

    fig.update_layout(
        title=f"3D Cloud Tracking for {city}",
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            projection=dict(type="natural earth"),
            center=dict(lat=lat, lon=lon),
            projection_scale=5,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig

# Layout of the Dash app
app.layout = html.Div([
    html.Div([
        html.H1("3D Cloud Tracking and Weather Information", className='title'),
        html.Div([
            # City Input field with animation
            dcc.Input(id='city-input', type='text', placeholder='Enter city name', debounce=True, className='city-input'),
            
            # 3D Globe (Map)
            dcc.Graph(id='3d-globe', config={'scrollZoom': True}, className='graph'),
        ], className='content-box'),
            # Slider for time-based cloud data change simulation
    dcc.Slider(
        id='time-slider',
        min=0,
        max=10,
        step=1,
        marks={i: str(i) for i in range(11)},
        value=0,
        className='slider'
    ),

        html.Div(id='weather-info', className='weather-info'),
    ], className='main-container'),


    # Footer
    html.Footer([
        html.P("Designed and Developed by ©Rishabh Tiwari (Coding Ninjas)", className='footer-text')
    ], className='footer')
])

# Callback to update both the 3D Globe and Weather Information
@app.callback(
    [Output('3d-globe', 'figure'),
     Output('weather-info', 'children')],
    [Input('time-slider', 'value'),
     Input('city-input', 'value')]
)
def update_figure_and_weather(time_value, city_name):
    if not city_name or city_name.strip() == "":
        return go.Figure(), []  # Return empty figure and no weather data
    
    # Fetch cloud data and coordinates for the given city
    cloud_data, lat, lon = get_cloud_data(city_name)
    if cloud_data is None:
        return go.Figure(), [html.P("City not found or no cloud data available.")]
    
    # Simulate cloud data change with time slider
    cloud_data += (time_value * 5)  # Simulated change in cloud coverage
    
    # Create the 3D globe
    fig = create_3d_globe(city_name, cloud_data, lat, lon)

    # Fetch weather data for the given city
    weather_data = get_weather_data(city_name)
    if weather_data is None:
        return go.Figure(), [html.P("Could not retrieve weather data. Please check the city name.")]
    
    weather_info = [
        html.H4(f"Weather Information for {city_name}"),
        html.P(f"Temperature: {weather_data['temperature_celsius']}°C / {weather_data['temperature_fahrenheit']}°F"),
        html.P(f"Feels Like: {weather_data['feels_like_celsius']}°C / {weather_data['feels_like_fahrenheit']}°F"),
        html.P(f"Humidity: {weather_data['humidity']}%"),
        html.P(f"Wind Speed: {weather_data['wind_speed']} m/s"),
        html.P(f"Description: {weather_data['description']}")
    ]
    
    return fig, weather_info

# Route to serve the frontend HTML page
@server.route('/')
def index():
    return redirect('/dash/')

# Run the Flask server
if __name__ == '__main__':
    with server.app_context():
        db.create_all()  # Ensure database tables are created
    server.run(debug=True)
