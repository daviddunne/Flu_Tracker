import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from utilities.text_classifier import TweetClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, NuSVC
from nltk.tokenize import word_tokenize


path_to_pickle_files = "pickle_files/"


def save_to_pickle_file(path, filename, object):
    try:
        file = open(path + filename, 'wb')
        pickle.dump(object, file)
        file.close()
    except IOError:
        print("error while opening file: " + path + filename)


def load_from_pickle_file(path, filename):
    try:
        file = open(path+filename, 'rb')
        obj = pickle.load(file)
        file.close()
    except IOError:
        print("Error while opening file: " + path + filename)
    return obj

word_features = load_from_pickle_file(path_to_pickle_files, "word_features.pickle")


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

feature_sets = load_from_pickle_file(path_to_pickle_files, "feature_sets.pickle")

random.shuffle(feature_sets)

training_set = feature_sets[:2000]
testing_set = feature_sets[2000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(50)
save_to_pickle_file(path_to_pickle_files, "original_NB_classifier.pickle", classifier)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "MNB_classifier.pickle", MNB_classifier)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "BernoulliNB_classifier.pickle", BernoulliNB_classifier)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "LogisticRegression_classifier.pickle", LogisticRegression_classifier)


SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "SGDClassifier_classifier.pickle", SGDClassifier_classifier)


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "LinearSVC_classifier.pickle", LinearSVC_classifier)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
save_to_pickle_file(path_to_pickle_files, "NuSVC_classifier.pickle", NuSVC_classifier)

voted_classifier = TweetClassifier("pickle_files/")
print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)