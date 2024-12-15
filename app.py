from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_KEY = "e236faf75d73924660f714085abd396e"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None
    city_details_url = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url_metric = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=en&appid={API_KEY}"
            url_imperial = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&lang=en&appid={API_KEY}"
            
             
            response_metric = requests.get(url_metric)
            response_imperial = requests.get(url_imperial)
            
            if response_metric.status_code == 200 and response_imperial.status_code == 200:
                weather_data = {
                    "metric": response_metric.json(),
                    "imperial": response_imperial.json()
                }
                city_details_url = f"https://openweathermap.org/city/{weather_data['metric']['id']}"
            else:
                error_message = "City not found. Please enter a valid city name."

    return render_template(
        "index.html", 
        weather_data=weather_data, 
        error_message=error_message, 
        city_details_url=city_details_url
    )


if __name__ == "__main__":
    app.run(debug=True)
