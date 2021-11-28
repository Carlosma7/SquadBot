from controller import *
from markups import *

import telebot
from dotenv import load_dotenv
import os
import re

# Telegram Bot Token from BotFather
# Get info from .env
load_dotenv(dotenv_path = '.env')
# Get Telegram bot token
TOKEN = os.getenv('TOKEN')

# Telebot Bot
bot = telebot.TeleBot(TOKEN)

# Bot controller
controller = Controller()

# Bot welcome
@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
	# Comprobar que la conversación es en un grupo
	if message.chat.type == 'group':
		bot.send_message(message.chat.id, f"Hi! Welcome everyone to SquadBot \U0001f916!\n\nI'm a Bot where friends' can rely on their common tasks! I hope you will find me useful \U0001f60a \n\n\u2757Please, start myself in a private chat to get things done well\u2757 \n\nTo ask me anything, please enter */functions*", parse_mode = 'Markdown')
	else:
		bot.send_message(message.chat.id, f"Hi! It's me *SquadBot* \U0001f916!\n\nI'm designed to work on group chats so just add me to yours and let me help you \U0001f60a", parse_mode = 'Markdown')
		controller.save_chat(message.chat.id, message.from_user.username)

# Bot functionalities list
@bot.message_handler(commands=['functions'])
def functions(message):
	# Check the chat is in a group
	if message.chat.type == 'group':
		# Get the functions markup
		markup = markup_functions()
		# Send message to group
		bot.send_message(message.chat.id, f"This is the list that SquadBot \U0001f916 currently supports: ", parse_mode = 'Markdown', reply_markup=markup)
	else:
		# Send message to group
		bot.send_message(message.chat.id, f"This is the list that SquadBot \U0001f916 currently supports: \n\n \U0001f381 *Secret Santa*", parse_mode = 'Markdown')

# Bot create a new Secret Santa
@bot.callback_query_handler(lambda call: call.data == 'secretsanta')
def create_secret_santa(call):

	try:
		# Create a new Secret Santa in controller
		controller.create_secret_santa(call.message.chat.id)
		# Delete previous message
		bot.delete_message(call.message.chat.id, call.message.id)
		# Success message
		answer = f"\U0001f381 Here we go! @{call.from_user.username} has started a new *Secret Santa* party! It's time to join and make some gifts \U0001f381"
		# Send message to group
		bot.send_message(call.message.chat.id, answer, parse_mode = 'Markdown')

		markup = markup_secret_santa()
		# New message
		answer = f"\U0001f381 *{call.message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n\n*Price Limit*: Not defined\n\n*Date*: Not defined\n\n*Message*: Not defined\n\nPlease choose one of the following options:"
		bot.send_message(call.message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')
		
	except Exception as error:
		# An error is given
		answer = str(error)
		# Send error message to group
		bot.send_message(call.message.chat.id, answer)

# Bot answer Secret Santa behaviour
@bot.callback_query_handler(lambda call: bool(re.match("ss[0-1]", call.data)))
def answer_secret_santa(call):

	try:
		# Check which option has been pressed
		if call.data == 'ss0':
			# Join the Secret Santa party
			controller.join_secret_santa(call.message.chat.id, call.from_user.username)

		elif call.data == 'ss1':
			# Leave the Secret Santa party
			controller.leave_secret_santa(call.message.chat.id, call.from_user.username)

		# Delete previous message
		bot.delete_message(call.message.chat.id, call.message.id)
		

	except Exception as error:
		# An error is given
		answer = str(error)
		# Send error message to group
		bot.send_message(call.message.chat.id, answer)

	# Print Secret Santa again
	markup = markup_secret_santa()

	# Get the current Secret Santa party
	ss = controller.get_secret_santa(call.message.chat.id)
	# Get list of friends joined
	friends = ""
	for f in ss.get_friends():
		friends += f"\U0001f381 {f}\n"
	# Get the price limit
	price_limit = ss.get_limit() if ss.get_limit() != 0 else "Not defined"
	# Get the date
	date = ss.get_date() if ss.get_date() is not None else "Not defined"
	# Get the message
	ss_message = ss.get_message() if ss.get_message() is not None else "Not defined"

	# New message
	answer = f"\U0001f381 *{call.message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n{friends}\n*Price Limit*: {price_limit}€\n\n*Date*: {date}\n\n*Message*: {ss_message}\n\nPlease choose one of the following options:"
	bot.send_message(call.message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')

# Bot set Secret Santa arguments
@bot.callback_query_handler(lambda call: bool(re.match("ss[2-4]", call.data)))
def set_secret_santa(call):

	try:
		if call.data == 'ss2':
			# Delete previous message
			bot.delete_message(call.message.chat.id, call.message.id)
			# Set price limit for gifts
			bot.send_message(call.message.chat.id, f"To set the price limit for the Secret Santa, just write:\n\n`/setlimit <price>`\n\n`/setlimit 15`", parse_mode = 'Markdown')

		elif call.data == 'ss3':
			# Delete previous message
			bot.delete_message(call.message.chat.id, call.message.id)
			# Set date for gifts
			bot.send_message(call.message.chat.id, f"To set the date for the Secret Santa, just write:\n\n`/setdate <dd/mm>`\n\n`/setdate 27/08`", parse_mode = 'Markdown')

		elif call.data == 'ss4':
			# Delete previous message
			bot.delete_message(call.message.chat.id, call.message.id)
			# Send new message to group
			bot.send_message(call.message.chat.id, f"To set the message for the Secret Santa, just write:\n\n`/setmessage <Insert message here>`\n\n`/setmessage Hello, this is the demo message, please join the Secret Santa!`", parse_mode = 'Markdown')

	except Exception as error:
		# An error is given
		answer = str(error)
		# Send error message to group
		bot.send_message(call.message.chat.id, answer)

# Bot finish Secret Santa behaviour
@bot.callback_query_handler(lambda call: bool(re.match("ss[5-6]", call.data)))
def finish_secret_santa(call):

	try:
		if call.data == 'ss5':
			# Remove actual Secret Santa party
			controller.remove_secret_santa(call.message.chat.id)
			# Delete previous message
			bot.delete_message(call.message.chat.id, call.message.id)
			bot.send_message(call.message.chat.id, f"Sadly, @{call.from_user.username} has decided to end the Secret Santa \U0001f622")

		elif call.data == 'ss6':
			# Start the Secret Santa party matches
			controller.define_secret_santa_matches(call.message.chat.id, call.from_user.username)
			# Delete previous message
			bot.delete_message(call.message.chat.id, call.message.id)
			# Final message to notify the lottery has been done
			bot.send_photo(call.message.chat.id, photo="https://github.com/Carlosma7/SquadBot/blob/main/doc/img/gift.jpg?raw=true", caption=f"Alrighty then! It's time for some gifts \U0001f381.\n\nI've sent you in a private chat the friend you are giving your gift with all the party info.", parse_mode = 'Markdown')

			# Get the Secret Santa object from the chat
			ss = controller.get_secret_santa(call.message.chat.id)

			# Get pairs
			pairs = ss.get_pairs()
			# Get message
			ss_message = ss.get_message()
			# Get limit price
			limit = ss.get_limit()
			# Get date
			date = ss.get_date()
			# Check chats to assert all users are registered in a private chat
			for user in pairs:
				user_chat = controller.get_char(user)

			# Send private message to each user
			for user in pairs:
				# Get user chat
				user_chat = controller.get_chat(user)
				bot.send_message(user_chat, f"{ss_message}\n\n@{user}, as a result of the Secret Santa \U0001f381 in *{call.message.chat.title}*, you have to give a present to: @{pairs[user]}\n\nPrice limit: {limit}€\n\nDate: {date}", parse_mode = 'Markdown')

			# Remove actual Secret Santa party
			controller.remove_secret_santa(call.message.chat.id)

	except Exception as error:
		# An error is given
		answer = str(error)
		# Send error message to group
		bot.send_message(call.message.chat.id, answer)

		# Print Secret Santa again
		markup = markup_secret_santa()

		# Get the current Secret Santa party
		ss = controller.get_secret_santa(call.message.chat.id)
		# Get list of friends joined
		friends = ""
		for f in ss.get_friends():
			friends += f"\U0001f381 {f}\n"
		# Get the price limit
		price_limit = ss.get_limit() if ss.get_limit() != 0 else "Not defined"
		# Get the date
		date = ss.get_date() if ss.get_date() is not None else "Not defined"
		# Get the message
		ss_message = ss.get_message() if ss.get_message() is not None else "Not defined"

		# New message
		answer = f"\U0001f381 *{call.message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n{friends}\n*Price Limit*: {price_limit}€\n\n*Date*: {date}\n\n*Message*: {ss_message}\n\nPlease choose one of the following options:"
		bot.send_message(call.message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')

# Bot Secret Santa set limit
@bot.message_handler(commands=['setlimit'])
def set_limit_secret_santa(message):
	# Check the chat is in a group
	if message.chat.type == 'group':
		try:
			# Set the limit for the open Secret Santa
			controller.set_limit_secret_santa(message.chat.id, int(message.text.split()[-1]))

			# Print Secret Santa again
			markup = markup_secret_santa()

			# Get the current Secret Santa party
			ss = controller.get_secret_santa(message.chat.id)
			# Get list of friends joined
			friends = ""
			for f in ss.get_friends():
				friends += f"\U0001f381 {f}\n"
			# Get the price limit
			price_limit = ss.get_limit() if ss.get_limit() != 0 else "Not defined"
			# Get the date
			date = ss.get_date() if ss.get_date() is not None else "Not defined"
			# Get the message
			ss_message = ss.get_message() if ss.get_message() is not None else "Not defined"

			# New message
			answer = f"\U0001f381 *{message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n{friends}\n*Price Limit*: {price_limit}€\n\n*Date*: {date}\n\n*Message*: {ss_message}\n\nPlease choose one of the following options:"
			bot.send_message(message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')

		except Exception as error:
			# Delete previous message
			bot.delete_message(message.chat.id, message.id - 1)
			# Send new message to group
			bot.send_message(message.chat.id, f"To set the price limit for the Secret Santa, just write:\n\n`/setlimit <price>`\n\n`/setlimit 15`", parse_mode = 'Markdown')

	else:
		# Send message to group
		bot.send_message(message.chat.id, f"You can't set the limit price of a Secret Santa in a private chat. Please add me to your group of friends first.")

# Bot Secret Santa set date
@bot.message_handler(commands=['setdate'])
def set_date_secret_santa(message):
	# Check the chat is in a group
	if message.chat.type == 'group':
		try:
			# Set the limit for the open Secret Santa
			controller.set_date_secret_santa(message.chat.id, message.text.split()[-1])

			# Print Secret Santa again
			markup = markup_secret_santa()

			# Get the current Secret Santa party
			ss = controller.get_secret_santa(message.chat.id)
			# Get list of friends joined
			friends = ""
			for f in ss.get_friends():
				friends += f"\U0001f381 {f}\n"
			# Get the price limit
			price_limit = ss.get_limit() if ss.get_limit() != 0 else "Not defined"
			# Get the date
			date = ss.get_date() if ss.get_date() is not None else "Not defined"
			# Get the message
			ss_message = ss.get_message() if ss.get_message() is not None else "Not defined"

			# New message
			answer = f"\U0001f381 *{message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n{friends}\n*Price Limit*: {price_limit}€\n\n*Date*: {date}\n\n*Message*: {ss_message}\n\nPlease choose one of the following options:"
			bot.send_message(message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')

		except Exception as error:
			# Delete previous message
			bot.delete_message(message.chat.id, message.id - 1)
			# Send new message to group
			bot.send_message(message.chat.id, f"To set the date for the Secret Santa, just write:\n\n`/setdate <dd/mm>`\n\n`/setdate 27/08`", parse_mode = 'Markdown')

	else:
		# Send message to group
		bot.send_message(message.chat.id, f"You can't set the date of a Secret Santa in a private chat. Please add me to your group of friends first.")

# Bot Secret Santa set message
@bot.message_handler(commands=['setmessage'])
def set_date_secret_santa(message):
	# Check the chat is in a group
	if message.chat.type == 'group':
		try:
			# Set the limit for the open Secret Santa
			controller.set_message_secret_santa(message.chat.id, message.text.split(' ', 1)[1])

			# Print Secret Santa again
			markup = markup_secret_santa()

			# Get the current Secret Santa party
			ss = controller.get_secret_santa(message.chat.id)
			# Get list of friends joined
			friends = ""
			for f in ss.get_friends():
				friends += f"\U0001f381 {f}\n"
			# Get the price limit
			price_limit = ss.get_limit() if ss.get_limit() != 0 else "Not defined"
			# Get the date
			date = ss.get_date() if ss.get_date() is not None else "Not defined"
			# Get the message
			ss_message = ss.get_message() if ss.get_message() is not None else "Not defined"

			# New message
			answer = f"\U0001f381 *{message.chat.title}* Secret Santa \U0001f381 \n\n*List of friends*:\n{friends}\n*Price Limit*: {price_limit}€\n\n*Date*: {date}\n\n*Message*: {ss_message}\n\nPlease choose one of the following options:"
			bot.send_message(message.chat.id, answer, reply_markup=markup, parse_mode = 'Markdown')

		except Exception as error:
			# Delete previous message
			bot.delete_message(message.chat.id, message.id - 1)
			# Send new message to group
			bot.send_message(message.chat.id, f"To set the message for the Secret Santa, just write:\n\n`/setmessage <Insert message here>`\n\n`/setmessage Hello, this is the demo message, please join the Secret Santa!`", parse_mode = 'Markdown')

	else:
		# Send message to group
		bot.send_message(message.chat.id, f"You can't set the message of a Secret Santa in a private chat. Please add me to your group of friends first.")


bot.infinity_polling()