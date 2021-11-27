class ExistingSecretSanta(Exception):
	"""Raised when there's already a Secret Santa party open in the group chat."""
	pass

class NonExistingSecretSanta(Exception):
	"""Raised when there's not a Secret Santa party open in the group chat."""
	pass

class UserInSecretSanta(Exception):
	"""Raised when an user has already joined a Secret Santa party."""
	pass

class UserNotInSecretSanta(Exception):
	"""Raised when an user has not joined a Secret Santa party."""

class NotEnoughFriendsInSecretSanta(Exception):
	"""Raised when there aren't enough players in a Secret Santa party. There should be at least three."""