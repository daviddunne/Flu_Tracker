#   Author: David Dunne,    Student Number: C00173649,      Created Dec 2015

import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class TweetClassifier(ClassifierI):
    def __init__(self, path_to_pickles):
        self.path_to_pickles = path_to_pickles
        self._classifiers = self.load_classifiers()
        self.word_features = self.load_word_features()

    def classify(self, features):
        """
        Classifies a text as either pos(person has flu) or neg(person does not have flu)
        :param features: Dictionary<string:bool>
        :return: "pos"/"neg": string
        """
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        """
        Returns a confidence figure based on how many classifiers voted for the result
        :param features:
        :return: confidence:float
        """
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    def load_classifiers(self):
        """
        Loads classifier objects from pickle files
        :return: classifiers:List<SklearnClassifier>
        """
        classifiers = []
        classifer_file_names = ['original_NB_classifier.pickle', 'MNB_classifier.pickle',
                      'BernoulliNB_classifier.pickle', 'LogisticRegression_classifier.pickle',
                      'SGDClassifier_classifier.pickle', 'LinearSVC_classifier.pickle',
                      'NuSVC_classifier.pickle']
        for classifier_name in classifer_file_names:
            classifier = self.read_from_pickle_file(self.path_to_pickles, classifier_name)
            if classifier is not None:
                classifiers.append(classifier)
        return classifiers

    def load_word_features(self):
        """
        Loads word features from pickle file
        :return: word_features:List<string>
        """
        word_features = self.read_from_pickle_file(self.path_to_pickles, "word_features.pickle")
        return word_features

    def read_from_pickle_file(self, path_to_pick_files, filename):
        """
        reads an object from a pickle file
        :param path_to_pick_files: string
        :param filename: string
        :return: loaded_object: Object
        """
        try:
            file = open(path_to_pick_files + filename, 'rb')
            loaded_object = pickle.load(file)
            file.close()
        except IOError:
            print('Error while opening file: ' + path_to_pick_files + filename)
            loaded_object = None
        return loaded_object

    def find_features(self, document):
        """
        Iterates trhough features and adds True/False label depending on if feature word present in document
        :param document: List<string>
        :return: features: Dictionary<string:bool>
        """
        words = word_tokenize(document)
        features = {}
        for w in self.word_features:
            features[w] = (w in words)
        return features

    def sentiment(self, text):
        """
        Gets the sentiment of the text, true if text sentiment is person who has the flu, false if otherwise
        :param text: string
        :return: True/False: bool
        """
        feats = self.find_features(text)
        text_class = self.classify(feats)
        if text_class == 'neg':
            return False
        return True
