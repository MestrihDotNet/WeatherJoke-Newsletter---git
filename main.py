from email.message import EmailMessage
import requests
import ssl
import smtplib
from jokeapi import Jokes
import asyncio
import os

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

api_file_dir = os.path.join(os.path.dirname(__file__), 'api_file')
API_KEY = open(os.path.join(api_file_dir, 'weather_api.txt'), 'r').read().strip()
EMAIL_SENDER = open(os.path.join(api_file_dir, 'email_sender.txt'), 'r').read().strip()
EMAIL_RECEIVER = open(os.path.join(api_file_dir, 'email_receiver.txt'), 'r').read().strip()
EMAIL_CREDENTIAL = open(os.path.join(api_file_dir, 'email_credential.txt'), 'r').read().strip()

CITY = "Graz"
url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY


def rounded_kelvin_to_celsius(kelvin):
    return "{:.1f}".format(kelvin - 273.15)


async def get_joke():
    j = await Jokes()  # Correctly instantiate the class
    joke = await j.get_joke()  # Retrieve a random joke

    if joke["type"] == "single":
        return joke["joke"]
    else:
        return f"{joke['setup']}<br><b>{joke['delivery']}</b>"


joke_text = asyncio.run(get_joke())

# Get weather data
response = requests.get(url).json()
temp_celsius = rounded_kelvin_to_celsius(response["main"]["temp"])
humidity = response["main"]["humidity"]
weather_status = response["weather"][0]["main"] + " - " + response["weather"][0]["description"]

# Get a random fox image
response_dog = requests.get("https://dog.ceo/api/breeds/image/random").json()
dog_image_url = response_dog["message"]

subject = "🌞 Your Daily Newsletter"

# HTML Email Body
body = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #007BFF;
        }}
        .weather {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        .image-container {{
            text-align: right;
            margin-top: 20px;
        }}
        .image-container img {{
            border-radius: 10px;
            width: 300px;
        }}
        .content {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .weather-info {{
            width: 60%;
        }}
        .joke {{
            width: 35%;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>☀️ Good Morning! Here’s your daily update 🌿</h1>

        <div class="content">
            <div class="weather-info">
                <div class="weather">
                    <p><strong>🌡 Temperature:</strong> {temp_celsius}°C</p>
                    <p><strong>💧 Humidity:</strong> {humidity}%</p>
                    <p><strong>⛅ Weather Status:</strong> {weather_status}</p>
                </div>

                <div class="joke">
                    <h2>Dark Joke of the Day!</h2>
                    <p>{joke_text}</p>
                </div>

                <!-- Move this here to bring it closer to the weather and joke sections -->
                <div class="weather">
                    <p><strong>Oh and have a lovely day! :)</strong></p>
                </div>
            </div>

            <div class="image-container">
                <h2>Here's a cute Doggo for you!</h2>
                <img src="{dog_image_url}" alt="Cute Dog">
            </div>
        </div>
    </div>
</body>
</html>
"""

# Create email
em = EmailMessage()
em["From"] = EMAIL_SENDER
em["To"] = EMAIL_RECEIVER
em["Subject"] = subject
em.set_content(body, subtype="html")  # Set content as HTML

# Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(EMAIL_SENDER, EMAIL_CREDENTIAL)
    smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, em.as_string())

print("Email sent successfully!")
