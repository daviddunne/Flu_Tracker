import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, path_to_pickles):
        self.path_to_pickles = path_to_pickles
        self._classifiers = self.load_classifiers()
        self.word_features = self.load_word_features()

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def load_classifiers(self):
        classifiers = []
        file_names = ['original_NB_classifier.pickle', 'MNB_classifier.pickle',
                      'BernoulliNB_classifier.pickle', 'LogisticRegression_classifier.pickle',
                      'SGDClassifier_classifier.pickle', 'LinearSVC_classifier.pickle',
                      'NuSVC_classifier.pickle']
        for classifier_name in file_names:
            classifier = self.read_from_pickle_file(self.path_to_pickles, classifier_name)
            if classifier is not None:
                classifiers.append(classifier)
        return classifiers

    def load_word_features(self):
        return self.read_from_pickle_file(self.path_to_pickles, "word_features.pickle")

    def read_from_pickle_file(self, path_to_pick_files, filename):
        try:
            file = open(path_to_pick_files + filename, 'rb')
            loaded_object = pickle.load(file)
            file.close()
        except IOError:
            print('Error while opening file: ' + path_to_pick_files + filename)
            loaded_object = None
        return loaded_object

    def find_features(self, document):
        words = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in words)
        return features

    def sentiment(self, text):
        feats = self.find_features(text)
        text_class = self.classify(feats)
        if text_class == 'neg':
            return False
        return True
