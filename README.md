# Weather Joke Newsletter

This program fetches weather data from the OpenWeatherMap API, adds a joke fetched from the JokeAPI, and includes a cute dog picture from an API. It then formats all of this information in an HTML format and sends it via email, making it look like a daily newsletter.

## Features
- **Weather Information**: Fetches weather data like temperature, humidity, and weather status for a specified city.
- **Joke of the Day**: Fetches a dark humor joke using the JokeAPI.
- **Cute Dog Picture**: Fetches a cute dog image from an API to brighten your day.
- **HTML Newsletter**: All the information is formatted in an attractive HTML format.
- **Email Sending**: Sends the formatted HTML newsletter via email to the recipient.

## Prerequisites

To run this project, you will need:
- **Python 3.x** installed on your machine.
- The following Python libraries:
  - `requests` – for making HTTP requests to the weather, joke, and dog APIs.
  - `smtplib` – for sending emails.
  - `email.message` – for formatting the email.
  - `ssl` – for secure email connections.

You can install the required libraries by running:
```bash
pip install requests jokeapi
