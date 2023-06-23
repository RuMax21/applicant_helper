import db_management

def analytics(func: callable):
	def analytics_wrapper(message):
		
		if not (db_management.is_user_checking(str(message.chat.id))):
			db_management.adding_new_user(str(message.chat.id))
		return func(message)

	return analytics_wrapper

def function_call_statistics(user_id, function_name):
	print(1)
	db_management.update_statistics(user_id, function_name)