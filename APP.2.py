import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests
from flask import Flask, render_template
from datetime import datetime

# Initialize Flask app and Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "your_api_key_here"

    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None  # Return None if city is not found or there is an error in the response

    temp_kelvin = response['main']['temp']
    temp_celsius = temp_kelvin - 273.15
    temp_fahrenheit = temp_celsius * (9 / 5) + 32

    weather_data = {
        'city': city,
        'temperature_celsius': round(temp_celsius, 2),
        'temperature_fahrenheit': round(temp_fahrenheit, 2),
        'humidity': response['main']['humidity'],
        'wind_speed': response['wind']['speed'],
        'description': response['weather'][0]['description']
    }
    return weather_data

# Function to get latitude and longitude from city name
def get_lat_lon(city):
    API_KEY = 'your_api_key_here'  # Your OpenWeatherMap API Key
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
    
    api_key = 'your_api_key_here'
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None, None, None  # Return None if API response is not successful
    
    data = response.json()
    clouds = data['clouds']['all']  # Cloud coverage percentage
    return clouds, lat, lon

# 3D Globe Rendering Function with Layered Textures
def create_3d_globe(city, cloud_data, lat, lon):
    # Earth daytime image and cloud overlay
    daymap_url = "/static/path_to_daymap.png"  # Path to the Daymap PNG
    cloudmap_url = "/static/path_to_cloudmap.png"  # Path to the Cloudmap PNG

    fig = go.Figure(go.Scattergeo(
        lat=[lat], lon=[lon],
        text=f"{city}\nCloud Coverage: {cloud_data}%",
        mode='markers+text',
        marker=dict(size=12, color='blue', opacity=0.7)
    ))

    # Add daymap as the base layer
    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="white",
        lakecolor="lightblue",
        center=dict(lat=lat, lon=lon),
        projection_scale=5,
        # Add the daymap image as the base texture
        layout=dict(
            images=[dict(
                source=daymap_url,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                sizex=1.5, sizey=1.5,  # Adjust size for the texture
                opacity=1, layer="below"
            )]
        )
    )

    # Add cloudmap as an overlay with some transparency
    fig.update_geos(
        layout=dict(
            images=[dict(
                source=cloudmap_url,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                sizex=1.5, sizey=1.5,  # Adjust size for cloud coverage
                opacity=0.6, layer="above"
            )]
        )
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
    html.H1("3D Cloud Tracking and Weather Information"),
    html.Div([
        # City Input field
        dcc.Input(id='city-input', type='text', placeholder='Enter city name', debounce=True),
        
        # 3D Globe (Map)
        dcc.Graph(id='3d-globe', config={'scrollZoom': True}),
        
        # Weather Information
        html.Div(id='weather-info', style={'marginTop': '20px'})
    ]),
])

# Callback to update both the 3D Globe and Weather Information
@app.callback(
    [Output('3d-globe', 'figure'),
     Output('weather-info', 'children')],
    [Input('city-input', 'value')]
)
def update_figure_and_weather(city_name):
    if not city_name or city_name.strip() == "":
        return go.Figure(), []  # Return empty figure and no weather data
    
    # Fetch cloud data and coordinates for the given city
    cloud_data, lat, lon = get_cloud_data(city_name)
    if cloud_data is None:
        return go.Figure(), [html.P("City not found or no cloud data available.")]
    
    # Create the 3D globe with layered textures
    fig = create_3d_globe(city_name, cloud_data, lat, lon)

    # Fetch weather data for the given city
    weather_data = get_weather_data(city_name)
    if weather_data is None:
        return go.Figure(), [html.P("Could not retrieve weather data. Please check the city name.")]
    
    weather_info = [
        html.H4(f"Weather Information for {city_name}"),
        html.P(f"Temperature: {weather_data['temperature_celsius']}°C / {weather_data['temperature_fahrenheit']}°F"),
        html.P(f"Humidity: {weather_data['humidity']}%"),
        html.P(f"Wind Speed: {weather_data['wind_speed']} m/s"),
        html.P(f"Description: {weather_data['description']}")
    ]
    
    return fig, weather_info

# Route to serve the frontend HTML page
@server.route('/')
def index():
    return render_template('index.html')

# Run the Flask server
if __name__ == '__main__':
    server.run(debug=True)
