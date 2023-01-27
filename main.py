import telebot
from telebot import types
from donationalerts import Alert
from dotenv import load_dotenv
from requests import get
from os import getenv


load_dotenv()

bottoken = getenv('BOT_TOKEN')
bot = telebot.TeleBot(bottoken)

tg_user_id = getenv('TG_UESR_ID')
da_alert_widget_token = getenv('DA_ALERT_WIGET_TOKEN')


Tname = ""


@bot.message_handler(commands=["start"])
def start(message):
	markup = types.ReplyKeyboardMarkup()
	hhelp = types.KeyboardButton("/help")
	global Tname
	Tname = str(message.chat.username)
	print(Tname)
	markup.add(hhelp)
	bot.send_message(
		message.chat.id, "Данный бот создан для помощи в оплате товаров и услуг.", reply_markup=markup, parse_mode="html"
	)  # старт и пояснение


@bot.message_handler(commands=["help"])
def help(massage):
	markup = types.ReplyKeyboardMarkup()
	fbuy = types.KeyboardButton("/buy")  # ссылка на оплату
	hstart = types.KeyboardButton("/start")  # старт
	hhelp = types.KeyboardButton("/help")  # вызов кнопок
	check = types.KeyboardButton("/check")  # кнопка проверки покупки
	markup.add(fbuy, hstart, hhelp, check)  # кнопки для помощи
	bot.send_message(massage.chat.id, "help button ↓", reply_markup=markup)


@bot.message_handler(commands=["buy"])
def Buy(massage):
	markup = types.InlineKeyboardMarkup()

	markup.add(types.InlineKeyboardButton("Buy VIP", url="https://www.donationalerts.com/r/larsymain"))
	bot.send_message(
		massage.chat.id, "для оплаты перейдите по ссылке (!при покупке укажите свой telegram username!):", reply_markup=markup, parse_mode="html"
	)  # ссылка на покупку


name = ""
_sum_ = ""

alert = Alert(da_alert_widget_token)


@alert.event()
def new_donation(event):
	get(
		f'https://api.telegram.org/bot{bottoken}/sendMessage?chat_id={tg_user_id}&text=Новый донат:\n{event.username} - {event.amount} {event.currency}\n{event.message}'
	)
	global name
	name = str({event.username})
	name = name[2:][:-2]

	global _sum_
	_sum_ = str({event.amount})
	_sum_ = _sum_[2:]
	_sum_ = _sum_[:-5]

	print(name, _sum_)


@bot.message_handler(commands=["check"])
def check(massage):
	if Tname == name and _sum_ == "50":
		bot.send_message(
			massage.chat.id, "ссылка на вход: https://t.me/+t8PFxUkd9thlODhi", parse_mode="html"
		)
	else:
		bot.send_message(
			massage.chat.id, "оплата не проведена", parse_mode="html"
		)


bot.polling(none_stop=True)
