import db_management
import datetime

def analytics(func: callable):
	def analytics_wrapper(message):
		
		if not (db_management.is_user_checking(db_management.hashing_of_name(str(message.chat.id)))):
			db_management.adding_new_user(str(message.chat.id), str(message.from_user.username))
		return func(message)

	return analytics_wrapper

def function_call_statistics(user_id, function_name):
	db_management.update_statistics(user_id, function_name)
	db_management.date_of_action(str(datetime.date.today()), function_name)
