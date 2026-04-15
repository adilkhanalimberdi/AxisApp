from flask import Blueprint, request, render_template
from src.services import weather_service

bp = Blueprint('weather', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/weather')
def weather():
    city = request.args.get('city', '').strip()

    if not city:
        return render_template('index.html', error_weather="Please specify a city!")

    lat, lng = weather_service.get_coordinates(city)

    if not lat or not lng:
        return render_template('index.html', error_weather="You must enter a correct city name!")

    weather_data = weather_service.fetch_weather(lat, lng)

    if not weather_data:
        return render_template('index.html', error_weather="Weather service is temporarily unavailable.")

    return render_template(
        'index.html',
        weather=weather_data,
        city=city.title(),
        forecast_days=len(weather_data)
    )