import time
import telebot
from telebot import types 

import config
import messages
import analytics

bot = telebot.TeleBot(config.TOKEN_INFO)

@bot.message_handler(commands=['start'])
@analytics.analytics
def start(message):
    markup = main_menu()
    bot.send_message(message.chat.id, 'Какая информация Вас интересует?', reply_markup=markup)

def main_menu():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton(messages.INFORMATION_ABOUT_ADMISSION_COMMISSION, callback_data='information_about_admission_commission'))
               # telebot.types.InlineKeyboardButton(messages.INFORMATION_ABOUT_CURRENT_POSITION_IN_RATING, callback_data='information_about_current_position_in_rating'))
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('information_about_admission_commission'))
def main_menu_callback(call):
	markup = submenu('information_about_admission_commission')
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
							text='Выберите интересующую информацию:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_WORK_SCHEDULE))
def work_schedule_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_WORK_SCHEDULE)
	markup = submenu('information_about_admission_commission')
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
						text=messages.WORK_SCHEDULE, reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_SUBMISSION_METHOD))
def submission_methods_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_SUBMISSION_METHOD)
	markup = submission_documents_button() 
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
						text='Подача документов', reply_markup=markup)

def submission_documents_button():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
			telebot.types.InlineKeyboardButton(messages.SUBMIT_IN_PERSON,
				callback_data='address_of_receiving'),
			telebot.types.InlineKeyboardButton(messages.POSTAL_SERVICE_OPERATORS,
				callback_data='postal_service_operators'),
			telebot.types.InlineKeyboardButton(messages.IN_ELECTRONIC_FORM,
				url=messages.IN_ELECTRONIC_FORM_LINK),
			telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='information_about_admission_commission')
			)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('address_of_receiving'))
def address_of_receiving_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
	text=messages.ADDRESS_OF_RECEIVING_DOCUMENTS, parse_mode='Markdown', reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('postal_service_operators'))
def postal_service_operators_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
	text=messages.POSTAL_SERVICE_OPERATORS_LINK, parse_mode='Markdown', reply_markup=create_button_one_back())


@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_EXAM_SCHEDULE))
def exam_schedule_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_EXAM_SCHEDULE)
	markup = exam_schedule_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите', reply_markup=markup)

def exam_schedule_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
		telebot.types.InlineKeyboardButton('СПО',
			url=messages.EXAM_SCHEDULE_LINK_SPK),
		telebot.types.InlineKeyboardButton('Бакалавриат/специалитет очно',
			url=messages.EXAM_SCHEDULE_LINK_BAC_SPEC_O),
		telebot.types.InlineKeyboardButton('Бакалавриат/специалитет заочно',
			url=messages.EXAM_SCHEDULE_LINK_BAC_SPEC_ZO),
		telebot.types.InlineKeyboardButton('Бакалавриат/специалитет очно-заочно',
			url=messages.EXAM_SCHEDULE_LINK_BAC_SPEC_OZO),
		telebot.types.InlineKeyboardButton('Магистратура',
			url=messages.EXAM_SCHEDULE_LINK_MAG),
		telebot.types.InlineKeyboardButton('Аспирантура',
			url=messages.EXAM_SCHEDULE_LINK_ASP),
		telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='information_about_admission_commission'))
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_LIST_TRAINING_AREAS))
def list_training_areas_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_LIST_TRAINING_AREAS)
	markup = list_training_areas_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
		text='Выберите уровень образования', reply_markup=markup)
			
def list_training_areas_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
			telebot.types.InlineKeyboardButton('СПО',
				url=messages.LIST_TRAINING_AREAS_LINK_SPK),
			telebot.types.InlineKeyboardButton('Бакалавриат',
				url=messages.LIST_TRAINING_AREAS_LINK_BAC),
			telebot.types.InlineKeyboardButton('Специалитет',
				url=messages.LIST_TRAINING_AREAS_LINK_SPEC),
			telebot.types.InlineKeyboardButton('Магистратура',
				url=messages.LIST_TRAINING_AREAS_LINK_MAG),
			telebot.types.InlineKeyboardButton('Аспирантура',
				url=messages.LIST_TRAINING_AREAS_LINK_ASP),
			telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='information_about_admission_commission')
			)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_MAIN_DATE))
def main_date_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_MAIN_DATE)
	markup = main_date_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
		text='Выберите уровень образования', reply_markup=markup)
	
def main_date_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
			telebot.types.InlineKeyboardButton('СПО',
				url=messages.MAIN_DATE_SPK),
			telebot.types.InlineKeyboardButton('Бакалавриат/Специалитет',
				url=messages.MAIN_DATE_BAC_SPEC),
			telebot.types.InlineKeyboardButton('Магистратура',
				url=messages.MAIN_DATE_MAG),
			telebot.types.InlineKeyboardButton('Аспирантура',
				url=messages.MAIN_DATE_ASP),
			telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='information_about_admission_commission')
			)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_DOCUMENTS_FOR_ADMISSION))
def documents_callback(call):
	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_DOCUMENTS_FOR_ADMISSION)
	markup = documents_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите подкатегорию:', reply_markup=markup)

def documents_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(telebot.types.InlineKeyboardButton('Бакалавриат/специалитет', callback_data='bac_documents_for_admission'),
	telebot.types.InlineKeyboardButton('Магистратура', callback_data='mag_documents_for_admission'),
	telebot.types.InlineKeyboardButton('Аспирантура', callback_data='asp_documents_for_admission'),
	telebot.types.InlineKeyboardButton('СПО', callback_data='spk_documents_for_admission'),
	telebot.types.InlineKeyboardButton('Назад', callback_data='information_about_admission_commission'))
	return markup

# @bot.callback_query_handler(func=lambda call: call.data.startswith(messages.CALLBACK_BUTTON_COST_OF_STUDY))
# def cost_of_study_callback(call):
# 	analytics.function_call_statistics(call.message.chat.id, messages.CALLBACK_BUTTON_COST_OF_STUDY)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bac_documents_for_admission'))
def bac_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=messages.DOCUMENTS_FOR_ADMISSION_BAC, reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('mag_documents_for_admission'))
def mag_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=messages.DOCUMENTS_FOR_ADMISSION_MAG, reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('asp_documents_for_admission'))
def asp_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=messages.DOCUMENTS_FOR_ADMISSION_ASP, reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('spk_documents_for_admission'))
def spk_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=messages.DOCUMENTS_FOR_ADMISSION_SPK, parse_mode='Markdown', reply_markup=create_button_one_back())

def submenu(category):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    if category == 'information_about_admission_commission':
        markup.add(telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_WORK_SCHEDULE, callback_data=messages.CALLBACK_BUTTON_WORK_SCHEDULE),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_SUBMISSION_METHOD, callback_data=messages.CALLBACK_BUTTON_SUBMISSION_METHOD),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_LIST_TRAINING_AREAS, callback_data=messages.CALLBACK_BUTTON_LIST_TRAINING_AREAS),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_DOCUMENTS_FOR_ADMISSION, callback_data=messages.CALLBACK_BUTTON_DOCUMENTS_FOR_ADMISSION),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_EXAM_SCHEDULE, callback_data=messages.CALLBACK_BUTTON_EXAM_SCHEDULE),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_MAIN_DATE, callback_data=messages.CALLBACK_BUTTON_MAIN_DATE),
                   telebot.types.InlineKeyboardButton(messages.MENU_BUTTON_COST_OF_STUDY, url=messages.COST_OF_STUDY_LINK),
        		   telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='btn_back'))
    elif category == 'information_about_current_position_in_rating':
        markup.add(telebot.types.InlineKeyboardButton('', callback_data=''),
        telebot.types.InlineKeyboardButton(messages.TEXT_BUTTON_BACK, callback_data='btn_back'))
    return markup

def create_button_back():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
		telebot.types.InlineKeyboardButton('Вернуться на начальную страницу', callback_data='btn_back_level_two')
	)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('btn_back'))
def button_back(call):
	markup = main_menu()
	bot.delete_message(call.message.chat.id,call.message.message_id)
	bot.send_message(call.message.chat.id, "Вы вернулись в меню",reply_markup=markup)
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('one_step_back'))
def button_back(call):
	bot.send_message(call.message.chat.id, "Вы вернулись в меню",reply_markup=create_button_one_back())

def create_button_one_back():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
			telebot.types.InlineKeyboardButton('Назад', callback_data='information_about_admission_commission')
		)
	return markup

bot.polling(none_stop=True, interval=0)