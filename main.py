import time
import telebot 

from telebot import types 

bot = telebot.TeleBot('6010195140:AAGlZib6TGsohjDlif5gEe4fmmd6qraatmU')

@bot.message_handler(commands=['start'])
def start(message):
    markup = main_menu()  # получаем клавиатуру с главным меню
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markup)

# функция для создания клавиатуры с главным меню
def main_menu():    
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)    
    markup.add(telebot.types.InlineKeyboardButton('Информация о приёмной комиссии', callback_data='main_category_1'),
               telebot.types.InlineKeyboardButton('Информация о текущем положении в рейтинге', callback_data='main_category_2'))
    return markup

# обработчик нажатия на кнопку главного меню
@bot.callback_query_handler(func=lambda call: call.data.startswith('main'))
def main_menu_callback(call):
    markup = sub1_menu(call.data.replace('main_', ''))  # получаем клавиатуру с подменю
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите интересующую информацию:', reply_markup=markup)

# обработчик нажатия на кнопку подменю
@bot.callback_query_handler(func=lambda call: call.data.startswith('working_time'))
def sub1_menu_callback(call):
    markup = sub1_menu(call.data.replace('sub1_', '')) 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='⏳ График работы: ⌛ \n \n Пн-Чт – 09:00 - 17:00 \n Пт – 09:00 - 16:00', reply_markup=create_button_one_back())
    #bot.send_message(call.message.chat.id,' ',)

# обработчик нажатия на кнопку под_под_меню
@bot.callback_query_handler(func=lambda call: call.data.startswith('number_phone'))
def sub2_menu_callback(call):
    #markup = sub_sub_menu(call.data.replace('sub2', '')) 
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='**🚙* Адрес **🚙* \n 394006, г. Воронеж, \n ул. 20-летия Октября, 84, \n к.1, ауд. 1002в, \n **☎* Телефон **☎* \n +7 (473) 271-53-15' + '\n \n' +
'**🚙* Адрес **🚙* \n 394026, г. Воронеж, \n Московский пр-т, 14, \n ауд. 219 \n **☎* Телефон **☎* \n +7 (473) 246-40-67'
'\n \n ✉ Также подать документы через операторов почтовой связи общего пользования можно по адресу: ✉ \n\n _394006, г. Воронеж, ул. 20-летия Октября, 84._ '
'\n \n 📧 Подробнее о подачи документов на обучение в электронной форме: 📧 \n\n https://cchgeu.ru/abiturientu/bak-spec/podacha-dokumentov/v-elektronnoy-forme/', parse_mode='Markdown',
reply_markup=create_button_one_back())

# обработчик нажатия на кнопку под_под_меню
# @bot.callback_query_handler(func=lambda call: call.data.startswith('address'))
# def sub3_menu_callback(call):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text='address')

@bot.callback_query_handler(func=lambda call: call.data.startswith('free_place'))
def free_place_callback(call):
	markup = free_place_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите уровень образования', reply_markup=markup)

def free_place_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(telebot.types.InlineKeyboardButton('Бакалавриат', callback_data='bac_plan'),
	telebot.types.InlineKeyboardButton('Cпециалитет', callback_data='spec_plan'),
	telebot.types.InlineKeyboardButton('Магистратура', callback_data='mag_plan'),
	telebot.types.InlineKeyboardButton('Аспирантура', callback_data='asp_plan'),
	telebot.types.InlineKeyboardButton('Назад', callback_data='main_category_1'))
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('bac_plan'))
def bac_plan_documents(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('ПЛАН ПРИЁМА БАКАЛАВРИАТ.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
@bot.callback_query_handler(func=lambda call: call.data.startswith('spec_plan'))
def spec_plan_documents(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('ПЛАН ПРИЕМА СПЕЦИАЛИТЕТ.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
@bot.callback_query_handler(func=lambda call: call.data.startswith('mag_plan'))
def mag_plan_documents(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('ПЛАН ПРИЁМА МАГИСТРАТУРА.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
@bot.callback_query_handler(func=lambda call: call.data.startswith('asp_plan'))
def asp_plan_documents(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('ПЛАН ПРИЁМА АСПИРАНТУРА.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())


# @bot.callback_query_handler(func=lambda call: call.data.startswith('dead_line'))
# def sending_pdf(call):


# 	doc = open('Бакалавриат и специалитет.pdf', 'rb')
# 	bot.send_document(call.message.chat.id, doc)

# 	doc1 = open('Магистры.pdf', 'rb')
# 	bot.send_document(call.message.chat.id, doc1)
	
# 	doc2 = open('Аспирантура.pdf', 'rb')
# 	bot.send_document(call.message.chat.id, doc2)

# 	doc.close()
# 	doc1.close()
# 	doc2.close()

# 	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
	

@bot.callback_query_handler(func=lambda call: call.data.startswith('dead_line'))
def sending_pdf(call):
	markup = sending_pdf_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите уровень образования', reply_markup=markup)

def sending_pdf_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(telebot.types.InlineKeyboardButton('Бакалавриат', callback_data='bac_spec_dead_line'),
	telebot.types.InlineKeyboardButton('Аспирантура', callback_data='asp_dead_line'),
	telebot.types.InlineKeyboardButton('Магистратура', callback_data='mag_dead_line'),
	telebot.types.InlineKeyboardButton('Назад', callback_data='main_category_1'))
	return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('bac_spec_dead_line'))
def bac_spec_dead_line_pdf(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('Бакалавриат и специалитет.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
@bot.callback_query_handler(func=lambda call: call.data.startswith('mag_dead_line'))
def mag_dead_line_pdf(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('Магистры.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())
@bot.callback_query_handler(func=lambda call: call.data.startswith('asp_dead_line'))
def asp_dead_line_pdf(call):
	bot.delete_message(call.message.chat.id,call.message.message_id)
	doc = open('Аспирантура.pdf', 'rb')
	bot.send_document(call.message.chat.id, doc)
	bot.send_message(call.message.chat.id, ' 🔙 ',reply_markup=create_button_one_back())



@bot.callback_query_handler(func=lambda call: call.data.startswith('documents'))
def documents_callback(call):
	markup = painting_buttons()
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите подкатегорию:', reply_markup=markup)
	# markup.add(telebot.types.InlineKeyboardButton('Бакалавриат/специалитет', callback_data='bac'),
	# telebot.types.InlineKeyboardButton('Магистратура', callback_data='mag'),
	# telebot.types.InlineKeyboardButton('Аспирантура', callback_data='asp'))
	# return markup
def painting_buttons():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(telebot.types.InlineKeyboardButton('Бакалавриат/специалитет', callback_data='bac'),
	telebot.types.InlineKeyboardButton('Магистратура', callback_data='mag'),
	telebot.types.InlineKeyboardButton('Аспирантура', callback_data='asp'),
	telebot.types.InlineKeyboardButton('Назад', callback_data='main_category_1'))
	return markup



@bot.callback_query_handler(func=lambda call: call.data.startswith('bac'))
def bac_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='❗ При подаче заявления о приеме поступающий представляет: ❗ \n\n'
'✅документ, удостоверяющий личность, гражданство; \n\n'
'✅документ об образовании и о квалификации, удостоверяющий образование соответствующего уровня, с приложением; \n\n'
'✅страховое свидетельство обязательного пенсионного страхования (при наличии); \n\n'
'✅фотографии поступающего 3х4 (рекомендуется в количестве 4 шт. черно-белые или цветные на усмотрение поступающего) \n\n'
'✅документы, подтверждающие наличие у поступающего прав: \n\n'
'✅на прием по результатам вступительных испытаний, проводимых ВГТУ самостоятельно; \n\n'
'✅на прием без вступительных испытаний или по особому преимуществу; \n\n'
'✅на прием в рамках особой или целевой квоты; \n\n'
'✅на преимущественное зачисление \n\n'
'✅документы, подтверждающие индивидуальные достижения (при их наличии); \n\n'
'✅иные документы (представляются по усмотрению поступающего).', reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('mag'))
def mac_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='❗ При подаче заявления о приеме поступающий представляет: ❗ \n\n'
'✅документ, удостоверяющий личность, гражданство; \n\n'
'✅документ об образовании и о квалификации, удостоверяющий образование соответствующего уровня, с приложением; \n\n'
'✅страховое свидетельство обязательного пенсионного страхования (при наличии); \n\n'
'✅фотографии поступающего 3х4 (рекомендуется в количестве 4 шт. черно-белые или цветные на усмотрение поступающего) \n\n'
'✅документы, подтверждающие наличие у поступающего прав: \n\n'
'✅на прием по результатам вступительных испытаний, проводимых ВГТУ самостоятельно; \n\n'
'✅на прием без вступительных испытаний или по особому преимуществу; \n\n'
'✅на прием в рамках особой или целевой квоты; \n\n'
'✅на преимущественное зачисление \n\n'
'✅документы, подтверждающие индивидуальные достижения (при их наличии); \n\n'
'✅иные документы (представляются по усмотрению поступающего).', reply_markup=create_button_one_back())

@bot.callback_query_handler(func=lambda call: call.data.startswith('asp'))
def asp_documents(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='❗ При подаче заявления, поступающий представляет следующие документы: ❗\n\n'
'✅документ, удостоверяющий личность, гражданство;\n\n'
'✅заявление на имя ректора о приеме в аспирантуру (формируется при подаче документов в программе 1С-университет);\n\n'
'✅документ о высшем образовании (диплом специалиста или магистра) или его копия с приложением;\n\n'
'✅страховое свидетельство обязательного пенсионного страхования (при наличии);\n\n'
'✅анкета;\n\n'
'✅протокол собеседования с предполагаемым научным руководителем по теме исследований/отзыв научного руководителя по опубликованным работам или реферату;\n\n'
'✅список опубликованных научных трудов, подписанный автором и предполагаемым научным руководителем;\n\n'
'✅документы, подтверждающие индивидуальные достижения (дипломы победителей олимпиад, научных конкурсов; патенты, свидетельства о регистрации программ и др.);\n\n'
'✅удостоверение о сдаче кандидатских экзаменов (при наличии);\n\n'
'✅копия паспорта (2-3 стр.);\n\n'
'✅4 фотографии.\n\n'
'✅при необходимости создания специальных условий при проведении вступительных испытаний – документ, подтверждающий инвалидность.\n\n', reply_markup=create_button_one_back())

# функция для создания клавиатуры с подменю
def sub1_menu(category):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    if category == 'category_1':
        markup.add(telebot.types.InlineKeyboardButton('🕑 Часы работы приёмной комиссии 🕑', callback_data='working_time'),
                   telebot.types.InlineKeyboardButton('🚙 Адреса и телефоны приемной комиссии 🚙', callback_data='number_phone'),
                   #telebot.types.InlineKeyboardButton('Адреса и способы подачи документов в ВГТУ', callback_data='address'),
                   telebot.types.InlineKeyboardButton('📑 Перечень направлений подготовки по факультетам и количество бюджетных мест 📑', callback_data='free_place'),
                   telebot.types.InlineKeyboardButton('🔥 Сроки подачи документов 🔥', callback_data='dead_line'),
                   # telebot.types.InlineKeyboardButton('Сроки проведения внутренних экзаменов', callback_data='inside_exams'),
                   telebot.types.InlineKeyboardButton('💼 Документы для поступления 💼', callback_data='documents'),
        		   telebot.types.InlineKeyboardButton('Назад', callback_data='btn_back'))
    elif category == 'category_2':
        markup.add(telebot.types.InlineKeyboardButton('-', callback_data='sub_subcategory_8'),
        telebot.types.InlineKeyboardButton('-', callback_data='sub_subcategory_9'),
        telebot.types.InlineKeyboardButton('Назад', callback_data='btn_back'))
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
	#markup = main_menu()
	#bot.delete_message(call.message.chat.id,call.message.message_id)
	bot.send_message(call.message.chat.id, "Вы вернулись в меню",reply_markup=create_button_one_back())

def create_button_one_back():
	markup = telebot.types.InlineKeyboardMarkup(row_width=1)
	markup.add(
			telebot.types.InlineKeyboardButton('Назад', callback_data='main_category_1')
		)
	return markup

bot.polling(none_stop=True, interval=0)