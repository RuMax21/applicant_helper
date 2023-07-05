import sqlite3
import hashlib
import datetime

def adding_new_user(user_id, username):
	user_id = hashing_of_name(user_id)
	username = hashing_of_name(username)
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
 
		if not(is_user_checking(username)):
			cursor.execute(f"INSERT INTO users (name_of_user, username, is_admin) VALUES('{user_id}', '{username}', 'False')")


def is_user_checking(username):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT name_of_user FROM users WHERE name_of_user = '{username}'")
		result = cursor.fetchall()
		if result:
			return True
		else:
			return False

def is_username_checking(username):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
		result = cursor.fetchall()
		if result:
			return True
		else:
			return False

def user_is_admin(username):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT is_admin FROM users WHERE name_of_user = '{username}'")
		result = cursor.fetchall()
		if len(result) != 0:
			if result[0][0].upper() == "FALSE":
				return False
			else:
				return True
		else:
			return False

def hashing_of_name(username):
	return ( (hashlib.md5(username.encode())).hexdigest() )

def calculate_total_requests():
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT SUM(working_time), SUM(submission_methods),"
		+ "SUM(list_training_areas), SUM(documents_for_admission), SUM(exam_schedule),"
		+ "SUM(important_date), SUM(cost_of_study) FROM users")
		result = cursor.fetchall()
		return result

def calculate_total_number_of_users():
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT COUNT(name_of_user) FROM users")
		result = cursor.fetchall()
		return result[0][0]

def get_value(username, command_name):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT {command_name} FROM users WHERE name_of_user = '{hashing_of_name(str(username))}'")
		result = cursor.fetchall()
		return result[0][0]

def update_statistics(username, command_name):

	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		if(is_user_checking(hashing_of_name(str(username)))):

			cursor.execute(f"UPDATE users SET '{command_name}' = '{get_value(username, command_name)}' + 1 WHERE name_of_user = '{hashing_of_name(str(username))}'")

def get_value_date(date, action):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT {action} FROM date_of_action WHERE date_action = '{date}'")
		result = cursor.fetchall()
		return result[0][0]

def date_of_action(date, action):
	was_find = True
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT date_action FROM date_of_action")
		result = cursor.fetchall()
		for i in result:
			if (str(date) == i[0]):
				was_find = False
				cursor.execute(f"UPDATE date_of_action SET '{action}' = '{get_value_date(date, action)}' + 1 WHERE date_action = '{date}'")
				break
		if was_find:
			cursor.execute(f"INSERT INTO date_of_action (date_action, '{action}') VALUES('{date}', 1)")

def find_date_in_db(date):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"SELECT * FROM date_of_action WHERE date_action = '{date}'")
		result = cursor.fetchall()
		if(len(result) != 0):
			return result[0]
		else:
			return False

def get_admin(username):
	with sqlite3.connect('db/analytics_db.db') as db:
		cursor = db.cursor()
		cursor.execute(f"UPDATE users SET is_admin = '{True}' WHERE username = '{username}'")
