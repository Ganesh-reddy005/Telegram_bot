import os
import telebot
BOT_TOKEN=os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(BOT_TOKEN)

#define a message handler that handles incoming /start and /hello
@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message,"Howday, How are you doing?")

@bot.message_handler(func=lambda message: True)
def smart_reply(message):
    if 'hello' in message.text.lower():
        bot.reply_to(message,"Hello there!")
    elif 'how are you' in message.text.lower():
        bot.reply_to(message,"I'm just a bot, but thanks for asking!")
    else:
        bot.reply_to(message,"I'm not sure how to respond to that.")

bot.infinity_polling()