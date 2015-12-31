class ValidatorClass:
    def __init__(self):
        self.banned_word_list = ['stomach', 'rt ', 'one direction', 'https', '@', 'the priest thinks']

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
        return True
