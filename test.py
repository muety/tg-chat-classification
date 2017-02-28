# -*- coding: utf-8 -*-

import pickle
from train_classifier import get_message_features

WORD_FEATURES_PATH = './output/word_features.pickle'


def load_classifier(path):
    f = open(path, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def load_word_features():
    f = open(WORD_FEATURES_PATH, 'rb')
    wf = pickle.load(f)
    f.close()
    return wf


def main():
    c1 = load_classifier('./output/classifier.pickle')
    wf = load_word_features()

    # -, j, p, j, p, j, j, m, p
    msgs = [u'some arbitrary chat message here']

    for m in msgs:
        print 'c1: ' + c1.classify(get_message_features(m.split(), wf, False))

if __name__ == "__main__":
    main()
