import telebot
import info
import json
from telebot import types
import random
token = "6655367298:AAH6TL7iuyWVkzf96jgSYM4ub5h49ZBiW-o"
changename = False
bot = telebot.TeleBot(token=token)
@bot.message_handler(commands=['start']) #/start
def start(message):
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton("Рассказать анекдот")
      btn2 = types.KeyboardButton("Доброе словцо")
      btn3 = types.KeyboardButton("Сплетни школы 192")
      btn4 = types.KeyboardButton("Сменить имя")
      markup.add(btn1, btn2, btn3, btn4)
      bot.send_message(message.chat.id, f"Привееееееет, {message.from_user.first_name}.\nЯ бот, с которым ты можешь хорошо провести время! Присоединяйся).")
      bot.send_message(message.chat.id, "Ниже ты увидишь кнопки для взаимодействия со мной.", reply_markup=markup)
      with open("users.json", "r") as f:
            users = json.load(f)
      if str(message.chat.id) not in users:
            users[message.chat.id] = {"id": message.chat.id}
      with open("users.json", "w") as f:
            json.dump(users, f, ensure_ascii=False)


@bot.message_handler(func=lambda a: changename is True)
def name(message):
      global changename
      with open("users.json", "r") as f:
            users = json.load(f)
      users[str(message.chat.id)]["name"] = message.text
      with open("users.json", "w") as f:
            json.dump(users, f, ensure_ascii=False)
      changename = False

@bot.message_handler(content_types=['text'])
def main(message):
      global changename
      if message.text == "Рассказать анекдот":
            bot.send_message(message.chat.id, info.jokes[random.randint(0, 6)])
      elif message.text == "Доброе словцо":
            bot.send_message(message.chat.id, info.good_words[random.randint(0, 5)])
      elif message.text == "Сплетни школы 192":
            bot.send_message(message.chat.id, "ДОСТУП ЗАПРЕЩЁН")
      elif message.text == "Сменить имя":
            changename = True
            bot.send_message(message.chat.id, "Следующее ваше сообщение будет использовано как ваше имя")

@bot.message_handler(content_types=['photo'])
def repeat_message(message):
      bot.send_photo(message.chat.id, message.photo[0].file_id)

bot.infinity_polling()