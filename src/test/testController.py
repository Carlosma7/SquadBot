import sys
import os
sys.path.append(os.path.abspath('./src/core/'))

from controller import *
import pytest
from assertpy import assert_that

# Test of creation of a Secret Santa
def test_create_secret_santa():
	# Create a Controller
	c = Controller()
	# Check that a Secret Santa doesn't exist
	assert_that(c.mongo.secretsantas.find({'chat': 'Test'}).count()).is_equal_to(0)
	# Create a new Secret Santa
	c.create_secret_santa('Test')
	# Check that a Secret Santa now exists
	assert_that(c.mongo.secretsantas.find({'chat': 'Test'}).count()).is_equal_to(1)
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test'})

# Test of joining an open Secret Santa
def test_join_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test2')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test2'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has no friends
	assert_that(ss.get_friends()).is_length(0)
	# Join a new friend in the party
	c.join_secret_santa('Test2', 'TestUser1')
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test2'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has one friend joined
	assert_that(ss.get_friends()).is_length(1)
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test2'})

# Test of leaving an open Secret Santa
def test_leave_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test3')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test3'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has no friends
	assert_that(ss.get_friends()).is_length(0)
	# Join a new friend in the party
	c.join_secret_santa('Test3', 'TestUser1')
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test3'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has one friend joined
	assert_that(ss.get_friends()).is_length(1)
	# Leave the party
	c.leave_secret_santa('Test3', 'TestUser1')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test3'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has no friends
	assert_that(ss.get_friends()).is_length(0)
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test3'})

# Test of defining the pairs of the Secret Santa lottery
def test_define_secret_santa_matches():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test4')
	# Join a new friend in the party
	c.join_secret_santa('Test4', 'TestUser1')
	# Join a new friend in the party
	c.join_secret_santa('Test4', 'TestUser2')
	# Join a new friend in the party
	c.join_secret_santa('Test4', 'TestUser3')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test4'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the pairs
	pairs = ss.get_pairs()
	# Set the pairs in the secret santa
	c.define_secret_santa_matches('Test4', 'TestUser1')
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test4'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has changed
	assert_that(pairs).is_not_equal_to(ss.get_pairs())
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test4'})

# Test of getting the list of friends of Secret Santa
def test_get_friends_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test5')
	# Join a new friend in the party
	c.join_secret_santa('Test5', 'TestUser1')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test5'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the list of friends
	friends = c.get_friends_secret_santa('Test5')
	# Check the two list of friends are equal
	assert_that(ss.get_friends()).is_equal_to(friends)
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test5'})

# Test of getting the pairs of Secret Santa
def test_get_pairs_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test6')
	# Join a new friend in the party
	c.join_secret_santa('Test6', 'TestUser1')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test6'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the list of friends
	pairs = c.get_pairs_secret_santa('Test6')
	# Check the two list of friends are equal
	assert_that(ss.get_pairs()).is_equal_to(pairs)
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test6'})

# Test of getting the object from a Secret Santa
def test_get_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test7')
	# Join a new friend in the party
	c.join_secret_santa('Test7', 'TestUser1')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test7'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the list of friends
	secret_santa = c.get_secret_santa('Test7')
	# Check the two list of friends are equal
	assert_that(ss.get_chat()).is_equal_to(secret_santa.get_chat())
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test7'})

# Test of removing a Secret Santa from database
def test_remove_secret_santa():
	# Create a Controller
	c = Controller()
	# Check that a Secret Santa doesn't exist
	assert_that(c.mongo.secretsantas.find({'chat': 'Test8'}).count()).is_equal_to(0)
	# Create a new Secret Santa
	c.create_secret_santa('Test8')
	# Check that a Secret Santa now exists
	assert_that(c.mongo.secretsantas.find({'chat': 'Test8'}).count()).is_equal_to(1)
	# Remove the Secret Santa
	c.remove_secret_santa('Test8')
	# Check that a Secret Santa doesn't exist
	assert_that(c.mongo.secretsantas.find({'chat': 'Test8'}).count()).is_equal_to(0)

# Test of setting the limit price of Secret Santa
def test_set_limit_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test9')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test9'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the limit
	limit = ss.get_limit()
	# Set the limit price in the secret santa
	c.set_limit_secret_santa('Test9', 1)
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test9'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has changed
	assert_that(limit).is_not_equal_to(ss.get_limit())
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test9'})

# Test of setting the date of Secret Santa
def test_set_date_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test10')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test10'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the date
	date = ss.get_date()
	# Set the limit price in the secret santa
	c.set_date_secret_santa('Test10', '22/02')
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test10'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has changed
	assert_that(date).is_not_equal_to(ss.get_date())
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test10'})

# Test of setting the message of Secret Santa
def test_set_message_secret_santa():
	# Create a Controller
	c = Controller()
	# Create a new Secret Santa
	c.create_secret_santa('Test11')
	# Get the created Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test11'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Get the message
	message = ss.get_message()
	# Set the limit price in the secret santa
	c.set_message_secret_santa('Test11', 'Test Message')
	# Get the updated Secret Santa
	ss = c.mongo.secretsantas.find_one({'chat': 'Test11'})
	# Create Secret Santa object from JSON
	ss = SecretSanta.from_dict(ss)
	# Check that the Secret Santa has changed
	assert_that(message).is_not_equal_to(ss.get_message())
	# Remove test Secret Santa from database
	c.mongo.secretsantas.delete_one({'chat': 'Test11'})

# Test of saving a private chat id
def test_save_chat():
	# Create a Controller
	c = Controller()
	# Check there aren't any chats created
	assert_that(c.mongo.chats.find({'chat': 'Test'}).count()).is_equal_to(0)
	# Create a new chat
	c.save_chat('Test', 'Test')
	# Check there is a chat created
	assert_that(c.mongo.chats.find({'chat': 'Test'}).count()).is_equal_to(1)
	# Remove test chat from database
	c.mongo.chats.delete_one({'chat': 'Test'})

# Test of getting a private chat id
def test_get_chat():
	# Create a Controller
	c = Controller()
	# Create a new chat
	c.save_chat('Test2', 'Test2')
	# Get the created chat
	chat = c.mongo.chats.find_one({'username': 'Test2'})
	# Get the chat
	chat2 = c.get_chat('Test2')
	# Check that they have the same chat
	assert_that(chat['chat']).is_equal_to(chat2)
	# Remove test chat from database
	c.mongo.chats.delete_one({'username': 'Test2'})
