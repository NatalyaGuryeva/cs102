import telebot

access_token = '654109257:AAH9BbqR7VSi4SxyiGt_ZtgUFu257B8kZ8E'
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
