# tg-chat-classification
__Machine Learning approach to classify the sender of [Telegram](http://telegram.org) chat messages__

## Steps (high-level overview)
1. Download Telegram message history using [tvdstaaij/telegram-history-dump](https://github.com/tvdstaaij/telegram-history-dump) together with [vysheng/tg](https://github.com/vysheng/tg) 
2. Extract message texts and message senders and dump them to JSON file (`extract_messages.py`)
3. Filter messages by minimum word length, filter stop words and build _(text, label)_ tuples, where _label_ is the name of the message's sender and _text_ is the respective message text. (`train.py::get_messages()`)
4. Compute features: binary feature (_contains_ / _contains not_) for every word in the entire message collection, as well as for every bi- and trigram (`train_classifier.py::compute_train_test()`). NOTE: Actually only top X most frequent words, bi- and trigrams are used as features because of complexity reasons.
5. Compute features for every message (n-dimensional vector with n = number of features = number of top X most frequent words, bigrams and trigrams)
6. Shuffle feature set. Divide into training set and test set (test set of length 5000).
7. Train [nltk.NaiveBayesClassifier](http://www.nltk.org/api/nltk.classify.html) classifier
8. Test and compute accuracy (`train.py::print_classifier_stats`)
9. Dump trained classifier as well as feature list.
9. Optional: Classify some hand-picked, new, unseen message (`test.py`)

## Optimization factors
* Training set size (number of messages for every chat partner)
* Feature vector dimensionality (number of words and ngrams to be used as binary features)
* Use single words, bigrams, trigrams or all of them
* Removing stopwords
* Minimum word length (2, 3, ...)
* ...

## Best result
* __|C| = 4__ (four classes, including three chat partners and myself)
* __|training set| = 37257__ (messages from chat partners: 7931, 9795, 9314, 10217)
* __|test set| = 5000__
* __|features| = 5000__ (3735 single words, 1201 bigrams, 64 trigrams)
* __min(|w|) = 2__ (minimum word length of 2, including Unicode emojis)
* __remove German stopwords__ (`nltk.corpus.stopwords.words('german')`)

... led to ...

* __Accuracy: 0.61__ = 61 %
* __Training time__: 348.26 sec

## Comparison to fastText
As a comparison baseline I've also trained a [fastText](https://github.com/facebookresearch/fastText) classifier. (`fasttext_preprocess.py` for preprocessing the messages to fasttext-compliant input format, `fasttext_train_test.py` to train fasttext, make predictions on the previously extracted test data and compute accuracy).
This led to an __accuracy of 0.6__, but with a very much better __training time of 0.66 sec__.

## Conclusion
61 % is certainly not a very reliable classifier, but at least significantly better than random guessing (chance of 1/4 in this case). Although having only very basic knowledge in machine learning (this project is kind of my first practical experiment in that area), I'd suppose that learning a person's chat writing style is way harder than [detecting the sentiment in a tweet](http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/) (that article originally inspired me) or [classifying news headlines to categories](https://github.com/facebookresearch/fastText#references). Actually it's not only hard to get a machine learn a chatting style, but also to do so as a human. Given a chat message without any semantic context, could you find out who of your friends is the sender? Probably not. But actually, the practical relevance of this project isn't quit high anyway, but it was a good practice for me to get into the basics of ML.

## Authors
* [Ferdinand Mütsch](https://ferdinand-muetsch.de), 2017