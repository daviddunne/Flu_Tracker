import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle


from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

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

path_to_pickle_files = "../classifiers/pickle_files/"


def save_to_pickle_file(path, filename, object):
    file = open(path + filename, 'wb')
    pickle.dump(object, file)
    file.close()

# J is adjective, r is adverb, and v is verb
allowed_word_types = ['J']


documents = []
all_words = []
try:
    positive_tweets = open("../classifiers/positive.txt", "r").read()
    for tweet in positive_tweets.split('\n'):
        documents.append((tweet, "pos"))
    positive_words = word_tokenize(positive_tweets)
    pos = nltk.pos_tag(positive_words)
    for word in pos:
        # check part of speech tag, this removes nouns and commas etc
        if word[1][0] in allowed_word_types:
            all_words.append(word[0])
except IOError:
    print("Error while opening: files/positive.txt")
try:
    negative_tweets = open("../classifiers/negative.txt", "r").read()
    for tweet in negative_tweets.split('\n'):
        documents.append((tweet, "neg"))
    negative_words = word_tokenize(negative_tweets)
    neg = nltk.pos_tag(negative_words)
    for word in neg:
         if word[1][0] in allowed_word_types:
            all_words.append(word[0])
except IOError:
    print("Error while opening: files/positive.txt")

# Save documents
save_to_pickle_file(path_to_pickle_files, "documents.pickle", documents)



all_words = nltk.FreqDist(all_words)


word_features = list(all_words.keys())[:5000]
#save word_features
save_to_pickle_file(path_to_pickle_files, 'word_features.pickle', word_features)


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

feature_sets = [(find_features(rev), category) for (rev, category) in documents]

# save feature_sets
save_to_pickle_file(path_to_pickle_files, "feature_sets.pickle", feature_sets)

random.shuffle(feature_sets)

training_set = feature_sets[:1800]
testing_set = feature_sets[1800:]

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

voted_classifier = VoteClassifier(
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)
print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)


def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats)


text = ["oh no I would have to get the flu now!",
        "get the flu shot this winter, it may save your life",
        "flu game ?",
        "there are really only two seasons.. allergy and flu.",
        "fucking flu killing me :(",
        "being hungover and having the flu is the worst thing possible 😖",
        "richarlison vai virar ídolo no flu...só se liguem",
        "if my daughter has the flu i'm killing whoever got her sick!"]

for t in text:
    print(t + ": " + sentiment(t))