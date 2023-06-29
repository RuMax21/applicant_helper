import telebot
from telebot import types

import config
import db_management
import messages

bot = telebot.TeleBot(config.TOKEN_ANALYTICS)

@bot.message_handler(commands=['start'])
def start(message):
	try:
		print(db_management.user_is_admin(db_management.hashing_of_name(str(message.chat.id))))
		if (db_management.is_user_checking(db_management.hashing_of_name(str(message.chat.id)))) & db_management.user_is_admin(db_management.hashing_of_name(str(message.chat.id))):
			markup = main_menu()
			bot.send_message(message.chat.id, 'Какая информация Вас интересует?', reply_markup=markup)
		else:
			bot.send_message(message.chat.id, 'Недостаточно прав!')
	except IndexError:
		bot.send_message(message.chat.id, 'Недостаточно прав!')

def main_menu():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
		telebot.types.InlineKeyboardButton('Общие количество запросов', callback_data=messages.CALLBACK_BUTTON_TOTAL_REQUESTS),
		telebot.types.InlineKeyboardButton('Статистика запросов по дате', callback_data=messages.CALLBACK_BUTTON_REQUESTS_OF_DATE),
		telebot.types.InlineKeyboardButton('Количество пользователей', callback_data=messages.CALLBACK_BUTTON_NUMBER_OF_USERS),
		telebot.types.InlineKeyboardButton('Выдать права на просмотр', callback_data=messages.CALLBACK_BUTTON_GIVE_OP)
		)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_TOTAL_REQUESTS))
def total_requests_callback(call):
	markup = create_button_back()
	list_of_statistics = db_management.calculate_total_requests()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
		text=
		f"Часы работы: '{list_of_statistics[0][0]}' \n"
		f"Способы подачи: '{list_of_statistics[0][1]}' \n"
		f"Перечень документов: '{list_of_statistics[0][2]}' \n"
		f"Документы для поступления: '{list_of_statistics[0][3]}' \n"
		f"Расписание: '{list_of_statistics[0][4]}' \n"
		f"Важные даты: '{list_of_statistics[0][5]}' \n"
		f"Стоимость обучения: '{list_of_statistics[0][5]}' \n"
	, reply_markup = markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_NUMBER_OF_USERS))
def number_of_users_callback(call):
	markup=create_button_back()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
		text=f"Количество пользователей: '{db_management.calculate_total_number_of_users()}'",
		reply_markup=markup)

def create_button_back():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
		telebot.types.InlineKeyboardButton('Назад', callback_data='btn_back')
	)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_REQUESTS_OF_DATE))
def requests_of_date_callback(call):
	msg = bot.send_message(call.message.chat.id, 'Введите дату в формате yyyy-mm-dd:')
	bot.register_next_step_handler(msg, inputed_message)

def inputed_message(message):
	answer_for_user = db_management.find_date_in_db(message.text)
	markup=create_button_back()
	if answer_for_user != False:
		bot.send_message(message.chat.id, 
			f"Информация по дате '{message.text}':\n"
			f"Часы работы: '{answer_for_user[2]}' \n"
			f"Способы подачи: '{answer_for_user[3]}' \n"
			f"Перечень документов: '{answer_for_user[4]}' \n"
			f"Документы для поступления: '{answer_for_user[5]}' \n"
			f"Расписание: '{answer_for_user[6]}' \n"
			f"Важные даты: '{answer_for_user[7]}' \n"
			f"Стоимость обучения: '{answer_for_user[8]}' \n"
			, reply_markup=markup)
	else:
		bot.send_message(message.chat.id, 'Дата отсутствует в базе!!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_GIVE_OP))
def give_op_callback(call):
	msg = bot.send_message(call.message.chat.id, 'Введите username пользователя')
	bot.register_next_step_handler(msg, user_for_op)

def user_for_op(message):
	is_username = db_management.is_username_checking(db_management.hashing_of_name(message.text))
	print(is_username)
	markup=create_button_back()
	if(is_username):
		db_management.get_admin(db_management.hashing_of_name(message.text))
		bot.send_message(message.chat.id, f"Пользователю {'@'+message.text} были выданы права на просмотр!!", reply_markup=markup)
	else:
		bot.send_message(message.chat.id, 'Пользователь отсутствует в базе!!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('btn_back'))
def button_back(call):
	markup = main_menu()
	bot.delete_message(call.message.chat.id,call.message.message_id)
	bot.send_message(call.message.chat.id, "Вы вернулись в меню",reply_markup=markup)
	return markup



bot.polling(none_stop=True, interval=0)
