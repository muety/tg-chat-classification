# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
import random
import train

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def messages_to_vectors(messages, min_word_length=1, remove_stopwords=False, adjust_self=False):
    vectors = []
    stop = set(stopwords.words('german'))
    num_in_messages = 0

    for label in messages:
        random.shuffle(messages[label])
        if (label == train.SELF_NAME): continue

        for msg in messages[label]:
            num_in_messages += 1
            split = [w for w in msg.split() if w.decode('utf-8') not in stop] if remove_stopwords else msg.split()
            vectors.append(([w.decode('utf-8') for w in split if len(w.decode('utf-8')) >= min_word_length], label.decode('utf-8')))

    c = 0
    avg = (num_in_messages / (len(messages.keys()) - 1))
    for msg in messages[train.SELF_NAME]:
        if c >= avg and adjust_self: break
        split = [w for w in msg.split() if w.decode('utf-8') not in stop] if remove_stopwords else msg.split()
        vectors.append(([w.decode('utf-8') for w in split if len(w.decode('utf-8')) >= min_word_length], train.SELF_NAME.decode('utf-8')))
        c += 1

    return vectors