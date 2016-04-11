#   Author: David Dunne,    Student Number: C00173649,      Created Dec 2015

from utilities.text_classifier import TweetClassifier


class ValidatorClass:
    """Used to validate text and location attributes of a tweet """
    def __init__(self, path_to_pickle_files):
        self.banned_word_list = ['rt ', 'https', 'jab']
        self.text_classifier = TweetClassifier(path_to_pickle_files)

    def validate_location(self, location):
        """
        Checks if location id None or "None"
        :param location: string
        :return: True/False: bool
        """
        if location is None:
            return False
        if location == 'None':
            return False
        return True

    def validate_text_from_tweet(self, text_from_tweet):
        """
        Checks if tweet is an empty string
        Checks if tweet contains banned words
        If above not true gets sentiment of text
        :param text_from_tweet:
        :return: True/False: bool
        """
        if text_from_tweet == '':
            return False
        for banned_word in self.banned_word_list:
            if banned_word in text_from_tweet:
                return False
        validText = self.text_classifier.sentiment(text_from_tweet)
        return validText

