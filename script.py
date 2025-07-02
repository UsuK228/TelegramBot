# ТГ бот версия 1, заброшено к хуям собачим т.к. telebot

import telebot
import requests
import logging
from bs4 import BeautifulSoup
import re

API_TOKEN = "YOUR TOKEN FROM BOTFATHER" # васдик иди нахуй

bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def safe_eval(expression):
    if not re.fullmatch(r'^[\d+-/().\s]+$', expression):
        return "Ошибка: допустимы только числа и операторы"
    try:
        return eval(expression)
    except Exception as err:
        return f"Ошибка : {err}"

def log_command(message):
    logger.info(
        f"Command: {message.text} | "
        f"User: {message.from_user.id} | "
        f"Username: @{message.from_user.username} | "
        f"Chat: {message.chat.id} ({message.chat.type})"
    )

@bot.message_handler(commands=["start"])
def send_welcome(message):
    log_command(message)
    bot.reply_to(message, """
Дарова кентофарик, напиши /help для подробной информации о мне!
""")

@bot.message_handler(commands=["help"])
def send_help(message):
    log_command(message)
    bot.reply_to(message, """
Я -- мультибот, могу выполнять разные задачи!
/start -- поздороваться
/calc [арифметический пример] -- калькулятор
/echo [сообщение] -- эхо
/oreshnik -- расчет полета ракеты "Орешник" с полигона "Капустин Яр" до Берлина
/status -- статус любимого сервера
/cubic -- кинуть кубик
""")

@bot.message_handler(commands=["calc"])
def send_calc(message):
    try:
        log_command(message)
        calc_expr = message.text.split(maxsplit=1)[1] #message.text.split(maxsplit=1)[1]
        bot.reply_to(message, safe_eval(calc_expr))
    except Exception as err:
        bot.reply_to(message, f"Ошибка: {err}")

@bot.message_handler(commands=["echo"])
def send_echo(message):
    log_command(message)
    try:
        user_text = message.text.split(maxsplit=1)[1]

        if "усик" in user_text.lower() or "usuk" in user_text.lower():
            bot.reply_to(message, "Запрещено писать имя императора!")
        else:
            bot.reply_to(message, message.text.split(maxsplit=1)[1])
    except Exception as err:
        bot.reply_to(message, f"Ошибка: {err}")

@bot.message_handler(commands=["oreshnik"])
def send_echo(message):
    log_command(message)
    bot.reply_to(message, "11-12 минут")
    bot.send_message(message.chat.id, "Хохлы пидоры")

@bot.message_handler(commands=["status"])
def send_status(message):
    log_command(message)
    url = "https://gmod-servers.com/server/262471/"

    response = requests.get(url)

    bs = BeautifulSoup(response.text, "lxml")
    players_info = bs.find("tbody")
    serverinfo = players_info.text
    data = serverinfo.split()

    status = data[6]
    count = data[12]
    mapname = data[22]
    checked = data[8]

    if count == "Online":
        count = 0
    if mapname == "Version":
        mapname = "Неизвестно"

    bot.send_message(message.chat.id, f"""
🔌IP сервера: 95.154.68.79:27015
🟢Статус: {status}
🎮Онлайн: {count}/32
🗺️Карта: {mapname}
🧐Последняя проверка: {checked} мин назад
""")

@bot.message_handler(commands=["cubic"])
def send_cubic(message):
    log_command(message)
    bot.send_dice(message.chat.id, "🎲")

@bot.message_handler(func=lambda message: True)
def log_text_messages(message):
    logger.info(f"Message: {message.text} | User: {message.from_user.id}")

if __name__ == "__main__":
    bot.infinity_polling()
    logger.info("Бот запущен и готов к работе!")