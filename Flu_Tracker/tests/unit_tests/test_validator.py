import unittest
from utilities.validator import ValidatorClass


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.test_validator = ValidatorClass()

    def test_validate_location_returns_False_when_location_is_None(self):
        self.assertFalse(self.test_validator.validate_location(None))

    def test_validate_location_returns_False_when_location_is_string_None(self):
        self.assertFalse(self.test_validator.validate_location('None'))

    def test_validate_location_returns_True_when_location_is_not_None(self):
        self.assertTrue(self.test_validator.validate_location('Dublin'))

    def validate_text_returns_True_when_text_contains_no_word_in_banned_word_list(self):
        self.assertTrue(self.test_validator.validate_text('valid text because has no banned words'))

    def validate_text_returns_False_when_text_is_empty(self):
        self.assertFalse(self.test_validator.validate_text(''))

    def validate_text_returns_False_when_text_contains_word_in_banned_word_list(self):
        self.assertFalse(self.test_validator.validate_text('invalid text because has word stomach'))
