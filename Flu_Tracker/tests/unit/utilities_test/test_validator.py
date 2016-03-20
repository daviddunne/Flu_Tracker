import os
import unittest

from utilities.context import project_root_dir
from utilities.validator import ValidatorClass

# Constants
path_to_pickle_files = os.path.join(project_root_dir, "classifiers/pickle_files/")


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.test_validator = ValidatorClass(path_to_pickle_files)

    def test_validate_location_returns_False_when_location_is_None(self):
        self.assertFalse(self.test_validator.validate_location(None))

    def test_validate_location_returns_False_when_location_is_string_None(self):
        self.assertFalse(self.test_validator.validate_location('None'))

    def test_validate_location_returns_True_when_location_is_not_None(self):
        self.assertTrue(self.test_validator.validate_location('Dublin'))

    def test_validate_text_returns_True_when_text_contains_no_word_in_banned_word_list(self):
        self.assertTrue(self.test_validator.validate_text_from_tweet('I have the flu!'))

    def test_validate_text_returns_False_when_text_is_empty(self):
        self.assertFalse(self.test_validator.validate_text_from_tweet(''))

    def test_validate_text_returns_False_when_text_contains_word_in_banned_word_list(self):
        self.assertFalse(self.test_validator.validate_text_from_tweet('invalid text because has rt meaning retweet'))
