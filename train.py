# -*- coding: utf-8 -*-

import extract_messages
import train_classifier
import os.path
import json
import utils
import pickle
import nltk
from datetime import datetime

CLASSIFIER_PATH = './output/classifier.pickle'
WORD_FEATURES_PATH = './output/word_features.pickle'
SELF_NAME = 'Ferdinand_Muetsch'

# Points to a directory, whoch contains (only) .jsonl files containing the messages downloaded with telegram-history-dump
RAW_DATA_PATH = './telegram-history-dump/output/json/'

# Where the filtered and preprocessed messages should be stored
FILTERED_DUMP_FILE = './data/filtered_dump.json'

def get_messages(min_word_length, remove_stopwords, adjust_self):
    raw_messages, messages = [], []
    if os.path.isfile(FILTERED_DUMP_FILE):
        with open(FILTERED_DUMP_FILE) as file:
            raw_messages = utils.byteify(json.load(file, encoding='utf-8'))
    else:
        raw_messages = extract_messages.extract(RAW_DATA_PATH, SELF_NAME)
        extract_messages.dump(FILTERED_DUMP_FILE)

    messages = utils.messages_to_vectors(raw_messages, min_word_length, remove_stopwords, adjust_self)
    print 'Number of messages\n----'
    c = 0
    for key in raw_messages:
        count = len([(m, k) for (m, k) in messages if k == key])
        print key + ': ' + str(count)
        c += count
    print 'Total: ' + str(c) + '\n----'

    return messages

def print_classifier_stats(classifier):
    train_set = train_classifier.train_set
    test_set = train_classifier.test_set
    start = datetime.now()
    print 'Accuracy on test set: ' + str(nltk.classify.accuracy(classifier, test_set))
    print 'Testing time: ' + str((datetime.now() - start).total_seconds()) + ' s'
    print classifier.show_most_informative_features(10)

def dump_classifier(classifier):
    f = open(CLASSIFIER_PATH, 'wb')
    pickle.dump(classifier, f)
    f.close()

def dump_word_features(word_features):
    f = open(WORD_FEATURES_PATH, 'wb')
    pickle.dump(word_features, f)
    f.close()

def main():
    messages = get_messages(min_word_length=2, remove_stopwords=True, adjust_self=True)
    train_classifier.compute_train_test(messages, top_features=5000, only_ngrams=False)
    classifier = train_classifier.train_classifier()
    dump_classifier(classifier)
    dump_word_features(train_classifier.word_features)
    print_classifier_stats(classifier)

if __name__ == "__main__": main()