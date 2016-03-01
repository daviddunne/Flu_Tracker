from utilities.database_handler import DatabaseHandler
import nltk
from nltk import word_tokenize
import pickle

path_to_pickle_files = "pickle_files/"


def save_to_pickle_file(path, filename, object):
    try:
        file = open(path + filename, 'wb')
        pickle.dump(object, file)
        file.close()
    except IOError:
        print("Error, failed to write to file: " + path + filename)


def write_to_file(filename, res):
    try:
        f = open(filename, 'w')
        for l in res:
            f.write(l['text'] + "\n")
        f.close()
    except IOError:
        print("cannot open file: " + filename)
print("Updating test data ... ")
dbh = DatabaseHandler()
res = dbh.get_tweets_with_sentiment('has flu')
print("Positive file updated")
write_to_file('positive.txt', res)

res = dbh.get_tweets_with_sentiment('no flu')
write_to_file('negative.txt', res)
print("Negative file updated")



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
print("Saving Documents ... ")
save_to_pickle_file(path_to_pickle_files, "documents.pickle", documents)
print("Documents Saved")


all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:5000]
#save word_features
print("Saving Word_Features ... ")
save_to_pickle_file(path_to_pickle_files, 'word_features.pickle', word_features)
print("Word_Features Saved")


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

feature_sets = [(find_features(rev), category) for (rev, category) in documents]

# save feature_sets
print("Saving Feature_Sets ... ")
save_to_pickle_file(path_to_pickle_files, "feature_sets.pickle", feature_sets)
print("Feature_Sets Saved")