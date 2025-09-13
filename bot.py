import os
from dotenv import load_dotenv
import telebot
import requests

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Welcome message handler
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello there!, to start using the bot, type /horoscope")

# Horoscope API call
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = 'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily'
    params = {'sign': sign.capitalize(), 'day': day.upper()}
    headers = {'accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# Horoscope command handler
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = ("What's your zodiac sign?\nChoose one:\n"
            "*Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*,\n"
            "*Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, *Pisces*")
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
    bot.register_next_step_handler(sent_msg, day_handler)

# Day selection handler
def day_handler(message):
    sign = message.text.strip()
    text = "Choose the day you want the horoscope for:\n*yesterday*, *today*, or *tomorrow*"
    sent_msg = bot.reply_to(message, text, parse_mode='Markdown')
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

# Final horoscope fetch and display
def fetch_horoscope(message, sign):
    day = message.text.strip()
    try:
        horoscope = get_daily_horoscope(sign, day)
        if 'data' in horoscope:
            data = horoscope['data']
            horoscope_msg = (f"*Horoscope:* {data['horoscope_data']}\n"
                             f"*Sign:* {sign}\n"
                             f"*Day:* {data['date']}")
            bot.send_message(message.chat.id, "Here is your horoscope:")
            bot.send_message(message.chat.id, horoscope_msg, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"Error: {horoscope.get('error', 'Unknown error')}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Oops! Something went wrong: {e}")

# Fallback handler for other messages
@bot.message_handler(func=lambda message: True)
def smart_reply(message):
    text = message.text.lower()
    if 'hello' in text:
        bot.reply_to(message, "Hello there!")
    elif 'how are you' in text:
        bot.reply_to(message, "I'm just a bot, but thanks for asking!")
    else:
        bot.reply_to(message, "I'm not sure how to respond to that.")

# Start polling
bot.infinity_polling()
