import datetime
from random import shuffle

# Secret Santa class
class SecretSanta():
	def __init__(self, chat: str):
		self.__chat = chat
		self.__friends = []
		self.__pairs = {}
		self.__limit = 0
		self.__date = None
		self.__message = None

	# Getter/Setter methods

	def get_friends(self):
		return self.__friends

	def get_pairs(self):
		return self.__pairs

	def get_limit(self):
		return self.__limit

	def set_limit(self, limit: int):
		self.__limit = limit

	def get_date(self):
		return self.__datetime

	def set_date(self, date: datetime.datetime):
		self.__date = date

	def get_message(self):
		return self.__message

	def set_message(self, message: str):
		self.__message = message

	# Add a new friend to the lottery
	def add_friend(self, name: str):
		"""Given a name of a new friend it adds him/her to the list of participants."""
		self.__friends.append(name)

	# Define the matches/pairs
	def define_matches(self):
		"""Define the different matches from the list of friends, checking that no one has himself/herself as the match."""
		for friend in self.__friends:
			self.__pairs[friend] = None

		shuffle(self.__friends)

		# Assign every person to the next person in the list, wrapping round if necessary
		for i in range(len(self.__friends)):
		    self.__pairs[self.__friends[i]] = self.__friends[i+1] if i+1 < len(self.__friends) else self.__friends[0]