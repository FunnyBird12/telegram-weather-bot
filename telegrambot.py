import telebot #library pyTelegramBotAPI
import requests
from datetime import date

BOT_TOKEN = "" #Enter your bot token
API_KEY = "" #Enter your api key

bot = telebot.TeleBot(BOT_TOKEN)
user_city = {}

@bot.message_handler(commands=['start'])
def start_weather(message):
    bot.send_message(message.chat.id, "Enter your city:")

@bot.message_handler(func=lambda message: True)
def get_city(message):
    city = message.text
    user_city[message.chat.id] = city

    today = date.today()

    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
        f"timeline/{city}/{today}/{today}"
        f"?unitGroup=metric&key={API_KEY}&contentType=json"
    )

    response = requests.get(url)

    if response.status_code != 200:
        bot.send_message(message.chat.id, "Error getting weather ")
        return

    data = response.json()

    temp = data["days"][0]["temp"]
    description = data["days"][0]["conditions"]

    bot.send_message(
        message.chat.id,
        f"⛅Weather in {city}:\n"
        f"Temperature: {temp}°C\n"
        f"Conditions: {description}"
    )

bot.infinity_polling()
