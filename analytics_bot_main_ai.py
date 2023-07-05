from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import db_management
import messages

storage = MemoryStorage()

bot = Bot(config.TOKEN_ANALYTICS)
dp = Dispatcher(bot=bot, storage=storage)

class Inputed_date(StatesGroup):
	date_for_finding = State()

class Inputed_username(StatesGroup):
	username_for_op = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	try:
		if (db_management.is_user_checking(db_management.hashing_of_name(str(message.chat.id)))) & db_management.user_is_admin(db_management.hashing_of_name(str(message.chat.id))):
			await bot.send_message(message.chat.id, 'Какая информация Вас интересует?', reply_markup=main_menu())
		else:
			await bot.send_message(message.chat.id, 'Недостаточно прав')
	except IndexError:
		await bot.send_message(message.chat.id, 'Недостаточно прав')

def main_menu():
	markup = InlineKeyboardMarkup(row_width=1)
	markup.add(
		InlineKeyboardButton('Общие количество запросов', callback_data=messages.CALLBACK_BUTTON_TOTAL_REQUESTS),
		InlineKeyboardButton('Статистика запросов по дате', callback_data=messages.CALLBACK_BUTTON_REQUESTS_OF_DATE),
		InlineKeyboardButton('Количество пользователей', callback_data=messages.CALLBACK_BUTTON_NUMBER_OF_USERS),
		InlineKeyboardButton('Выдать права на просмотр', callback_data=messages.CALLBACK_BUTTON_GIVE_OP)
		)
	return markup

@dp.callback_query_handler()
async def callback_query_main_menu(callback_query: types.CallbackQuery):
	if callback_query.data == messages.CALLBACK_BUTTON_TOTAL_REQUESTS:
		markup = create_button_back()
		list_of_statistics = db_management.calculate_total_requests()
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
		text=
		f"Часы работы: '{list_of_statistics[0][0]}' \n"
		f"Способы подачи: '{list_of_statistics[0][1]}' \n"
		f"Перечень документов: '{list_of_statistics[0][2]}' \n"
		f"Документы для поступления: '{list_of_statistics[0][3]}' \n"
		f"Расписание: '{list_of_statistics[0][4]}' \n"
		f"Важные даты: '{list_of_statistics[0][5]}' \n"
		f"Стоимость обучения: '{list_of_statistics[0][5]}' \n"
	, reply_markup = markup)

	elif callback_query.data == messages.CALLBACK_BUTTON_REQUESTS_OF_DATE:
		await bot.send_message(callback_query.message.chat.id, 'Введите дату в формате yyyy-mm-dd:')
		await Inputed_date.date_for_finding.set()


	elif callback_query.data == messages.CALLBACK_BUTTON_NUMBER_OF_USERS:
		markup=create_button_back()
		await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
		text=f"Количество пользователей: '{db_management.calculate_total_number_of_users()}'",
		reply_markup=markup)

	elif callback_query.data == messages.CALLBACK_BUTTON_GIVE_OP:
		await bot.send_message(callback_query.message.chat.id, 'Введите username пользователя')
		await Inputed_username.username_for_op.set()

	elif callback_query.data == 'btn_back':
		markup = main_menu()
		await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
		await bot.send_message(callback_query.message.chat.id, "Вы вернулись в меню",reply_markup=markup)
		return markup

@dp.message_handler(state=Inputed_date.date_for_finding)
async def writing_date(message: types.message, state: FSMContext) -> None:
	answer_for_user = db_management.find_date_in_db(message.text)
	markup=create_button_back()

	if answer_for_user != False:
		await bot.send_message(message.chat.id, 
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
		await bot.send_message(message.chat.id, 'Дата отсутствует в базе!!', reply_markup=markup)

	await state.finish()

@dp.message_handler(state=Inputed_username.username_for_op)
async def user_for_op(message: types.message, state: FSMContext) -> None:
	is_username = db_management.is_username_checking(db_management.hashing_of_name(message.text))
	markup=create_button_back()
	if(is_username):
		db_management.get_admin(db_management.hashing_of_name(message.text))
		await bot.send_message(message.chat.id, f"Пользователю {'@'+message.text} были выданы права на просмотр!!", reply_markup=markup)
	else:
		await bot.send_message(message.chat.id, 'Пользователь отсутствует в базе!!', reply_markup=markup)
	
	await state.finish()

def create_button_back():
	markup = InlineKeyboardMarkup(row_width=1)
	markup.add(
		InlineKeyboardButton('Назад', callback_data='btn_back')
	)
	return markup

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)