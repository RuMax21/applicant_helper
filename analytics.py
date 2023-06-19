import logging

def analytics(func: callable):
	users = set()
	def analytics_wrapper(message):
		
		if message.chat.id not in users:
			users.add(message.chat.id)
			print(users)
		
		return func(message)

	return analytics_wrapper

def function_call_statistics(user_id, function_name):
	print(user_id, function_name)