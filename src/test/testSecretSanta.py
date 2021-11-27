import sys
import os
sys.path.append(os.path.abspath('./src/core/'))

from secretsanta import SecretSanta
import pytest
from assertpy import assert_that

# Test to check if a friend is added to the list
def test_add_friend():
	ss = SecretSanta('Test')

	# Check there aren't any friends on the list
	assert_that(ss.get_friends()).is_empty()

	# Add a new friend called 'Test'
	ss.add_friend('Test')

	# Check there aren't any friends on the list
	assert_that(ss.get_friends()).is_not_empty()

# Test to check the matches have been defined properly
def test_define_matches():
	ss = SecretSanta('Test')

	# Add three friends
	ss.add_friend('Test1')
	ss.add_friend('Test2')
	ss.add_friend('Test3')

	# Define the matches
	ss.define_matches()

	# Get the matches
	matches = ss.get_pairs()

	# Check matches are not empty
	assert_that(matches).is_not_empty()
	# Check a friend is not matched with himself/herself
	assert_that(matches).does_not_contain_entry({'Test1':'Test1'},{'Test2':'Test2'},{'Test3':'Test3'})