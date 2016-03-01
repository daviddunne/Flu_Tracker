from utilities.text_classifier import VoteClassifier


class ValidatorClass:
    def __init__(self, path_to_pickle_files):
        self.banned_word_list = ['rt ', 'https']
        self.text_classifier = VoteClassifier(path_to_pickle_files)

    def validate_location(self, location):
        if location is None:
            return False
        if location == 'None':
            return False
        return True

    def validate_text(self, text):
        if text == '':
            return False
        for words in self.banned_word_list:
            if words in text:
                return False
        text_class = self.text_classifier.sentiment(text)
        return text_class

