from secretsanta import SecretSanta
from exceptions import *

import os
from dotenv import load_dotenv
import pymongo
import datetime

# Obtain info from .env
load_dotenv(dotenv_path = '.env')
# Get MongoDB token for MongoDB Atlas
MONGO_TOKEN = os.getenv('MONGO')

# Define a client
client = pymongo.MongoClient(MONGO_TOKEN, serverSelectionTimeoutMS = 2000)
# Define the database
database = client.SquadBot

# Controller class
class Controller():

	# Define the conection to MongoDB Atlas
	mongo = database

	# Create a new Secret Santa party
	def create_secret_santa(self, chat: str):
		"""Creates a new list for Secret Santa party, checking there isn't one open created previously."""

		# Check there isn't an open Secret Santa in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if not ss_found:
			# Create a new Secret Santa party
			new_ss = SecretSanta(chat)
			self.mongo.secretsantas.insert_one(new_ss.to_dict())
		else:
			raise ExistingSecretSanta('There is already an open Secret Santa in the group chat.')

	# Join a new Secret Santa party
	def join_secret_santa(self, chat: str, username: str):
		"""Joins a new friend to the Secret Santa party, checking if already exists in the group chat
		and the user has not joined previously."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Check the username is not in list
			if username not in ss.get_friends():
				ss.add_friend(username)

				# Update in database
				self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
			else:
				raise UserInSecretSanta(f'{username} has already joined the Secret Santa list.')
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Leave a Secret Santa party
	def leave_secret_santa(self, chat: str, username:str):
		"""Leave the current Secret Santa party, checking if the user is already on the party."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Check the username is in list
			if username in ss.get_friends():
				ss.remove_friend(username)

				# Update in database
				self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
			else:
				raise UserNotInSecretSanta(f'{username} cannot leave the Secret Santa party because he is not joined.')
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Define Secret Santa matches
	def define_secret_santa_matches(self, chat: str, username: str):
		"""Starts the lottery of Secret Santa party and defines the matches."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Check the username is in list
			if username in ss.get_friends():
				# Check there are at least three friends in the party
				if len(ss.get_friends()) >= 3:
					ss.define_matches()

					# Update in database
					self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
				else:
					raise NotEnoughFriendsInSecretSanta('There are not enough friends to start the Secret Santa party. There should be at least three of them.')
			else:
				raise UserNotInSecretSanta(f'{username} cannot start the Secret Santa party because he is not joined.')
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Get the list of the Secret Santa party integrants
	def get_friends_secret_santa(self, chat: str):
		"""Returns the list of the friends that had joined the Secret Santa party."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			return ss.get_friends()
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Get the pairs of the Secret Santa party
	def get_pairs_secret_santa(self, chat: str):
		"""Returns the pairs of the friends that had joined the Secret Santa party."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			return ss.get_pairs()
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Get a Secret Santa party object
	def get_secret_santa(self, chat: str):
		"""Returns the whole instance of a Secret Santa party from the chat if it exists."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			return ss
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Remove Secret Santa party
	def remove_secret_santa(self, chat: str):
		"""Removes all the information from the Secret Santa."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			# Remove Secret Santa party from database
			self.mongo.secretsantas.delete_one({'chat': chat})
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Set the limit for the Secret Santa party
	def set_limit_secret_santa(self, chat: str, limit: int):
		"""Sets the limit of price for the Secret Santa."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Set the new limit price
			ss.set_limit(limit)

			# Update in database
			self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Set the date for the Secret Santa party
	def set_date_secret_santa(self, chat: str, date: datetime.datetime):
		"""Sets the date for the Secret Santa."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Set the new date
			ss.set_date(date)

			# Update in database
			self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Set the message for the Secret Santa party
	def set_message_secret_santa(self, chat: str, message: str):
		"""Sets the message for the Secret Santa."""

		# Check there's an open Secret Santa party in the group chat
		ss = self.mongo.secretsantas.find_one({'chat': chat})
		ss_found = (ss != None)

		if ss_found:
			ss = SecretSanta.from_dict(ss)

			# Set the new message
			ss.set_message(message)

			# Update in database
			self.mongo.secretsantas.update({'chat': ss.get_chat()}, {'$set': ss.to_dict()})
		else:
			raise NonExistingSecretSanta('There is not an open Secret Santa in the group chat. Please create one first then join it.')

	# Save the private chat id from an user
	def save_chat(self, chat: str, username: str):
		"""Saves the private chat id from a conversation with an user to contact him/her later."""

		# Check there is a private chat already for that user
		user = self.mongo.chats.find_one({'username': username})
		user_found = (user != None)

		if user_found:
			# Modify the private chat id related to the user
			user['chat'] = chat

			# Update in database
			self.mongo.chats.update({'username': username}, {'$set': user})

		else:
			# Save the private chat id related to the user
			user = {'username': username, 'chat': chat}

			# Save in database
			self.mongo.chats.insert_one(user)

	# Get the private chat id from an user
	def get_chat(self, username: str):
		"""Gets the private chat id from a conversation with an user to contact him/her."""

		# Check there is a private chat already for that user
		user = self.mongo.chats.find_one({'username': username})
		user_found = (user != None)

		if user_found:

			return user['chat']

		else:
			raise UserHasNotStartedBotError('{username} cannot be contacted because he has not started the bot in a private conversation.')
