from utilities.text_classifier import VoteClassifier


class ValidatorClass:
    def __init__(self, path_to_pickle_files):
        self.banned_word_list = ['rt ', 'https', 'jab']
        self.text_classifier = VoteClassifier(path_to_pickle_files)

    def validate_location(self, location):
        if location is None:
            return False
        if location == 'None':
            return False
        return True

    def validate_text_from_tweet(self, text_from_tweet):
        if text_from_tweet == '':
            return False
        for banned_word in self.banned_word_list:
            if banned_word in text_from_tweet:
                return False
        text_classification = self.text_classifier.sentiment(text_from_tweet)
        return text_classification

