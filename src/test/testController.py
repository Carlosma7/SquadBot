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
