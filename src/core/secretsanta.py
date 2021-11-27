import datetime
from random import shuffle
from typing import List

# Secret Santa class
class SecretSanta():
	def __init__(self, chat: str):
		self.__chat = chat
		self.__friends = []
		self.__pairs = {}
		self.__limit = 0
		self.__date = None
		self.__message = None

	# from_dict JSON constructor
	@classmethod
	def from_dict(cls, data: dict):
		ss = cls(data.get('chat'))
		ss.set_friends(data.get('friends'))
		ss.set_pairs(data.get('pairs'))
		ss.set_limit(data.get('limit'))
		ss.set_date(data.get('date'))
		ss.set_message(data.get('message'))
		return ss

	# Getter/Setter methods

	def get_chat(self):
		return self.__chat

	def get_friends(self):
		return self.__friends

	def set_friends(self, friends: List):
		self.__friends = friends

	def get_pairs(self):
		return self.__pairs

	def set_pairs(self, pairs: dict):
		self.__pairs = pairs

	def get_limit(self):
		return self.__limit

	def set_limit(self, limit: int):
		self.__limit = limit

	def get_date(self):
		return self.__date

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

	# Remove a friend from the lottery
	def remove_friend(self, name: str):
		"""Given a name of a friend it removes him/her from the list of participants."""
		self.__friends.remove(name)

	# Define the matches/pairs
	def define_matches(self):
		"""Define the different matches from the list of friends, checking that no one has himself/herself as the match."""
		for friend in self.__friends:
			self.__pairs[friend] = None

		shuffle(self.__friends)

		# Assign every person to the next person in the list, wrapping round if necessary
		for i in range(len(self.__friends)):
		    self.__pairs[self.__friends[i]] = self.__friends[i+1] if i+1 < len(self.__friends) else self.__friends[0]

	# JSON to_dict conversion
	def to_dict(self):
		return {'chat': self.get_chat(), 'friends': self.get_friends(), 
		'pairs': self.get_pairs(), 'limit': self.get_limit(), 
		'date': self.get_date(), 'message': self.get_message()}
