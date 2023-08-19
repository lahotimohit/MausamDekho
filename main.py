import requests
import currentwether
import weather_forecast
from flask import Flask, render_template, request, redirect, url_for

BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY ="578de6b540aaa3318e45bb44fb173cce"

lat = []
long = []
state = []
require_lat = None
require_long = None

app = Flask(__name__)


def geo_finder(city, state_choice, counter):
    params = {
        'q': city,
        'limit': 10,
        'appid': API_KEY
    }
    response = requests.get(url=BASE_URL, params=params).json()
    size = len(response)

    for item in range(size):
        lat.append(response[item]['lat'])
        long.append(response[item]['lon'])
        state.append(response[item]['state'])

    for item in range(len(state)):
        if state[item] == state_choice.title():
            require_lat = lat[item]
            require_long = long[item]
            counter += 1
            return {'latitude': require_lat, 'longitude': require_long}

    if counter == 0:
        return {'latitude': 'not defined', 'longitude': 'not defined'}


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city_name = request.form.get('city')
        state_name = request.form.get('state')

        return redirect(url_for('weather', city=city_name, user_state=state_name))  
    return render_template('index.html')



@app.route('/weather/<city>/<user_state>')
def weather(city, user_state):
    return render_template('weather.html', u_city=city, u_state=user_state)


@app.route('/button_clicked/<city>/<state_choice>/<option>', methods=['POST', 'GET'])
def button_clicked(city, state_choice, option):
    output = geo_finder(city=city, state_choice=state_choice, counter=0)
    latitude = output['latitude']
    longitude = output['longitude']

    if option == 'current':
        cw = currentwether.CurrentWeather(latitude=latitude, longitude=longitude)
        response_curr = cw.current_weather()
        return render_template("current.html", data=response_curr)

    elif option == 'forecast':
        fw = weather_forecast.WeatherForecast(latitude=latitude, longitude=longitude)
        response_curr = fw.weather_forecast()
        return render_template('forecast.html', output=response_curr)

    else:
        response = "Unknown button clicked!"

    return response


if __name__ =="__main__":
    app.run(debug=True)
