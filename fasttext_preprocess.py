import json
import os.path
import utils
import random
import extract_messages

FASTTEXT_TRAIN_FILE = './data/fasttext.train.txt'
FASTTEXT_TEST_FILE = './data/fasttext.test.txt'
FASTTEXT_TEST_VALIDATION_FILE = './data/fasttext.test_validation.txt'
FILTERED_DUMP_FILE = './data/filtered_dump.json'
RAW_DATA_PATH = './telegram-history-dump/output/json/'
SELF_NAME = 'Ferdinand_Muetsch'

messages = []

if os.path.isfile(FILTERED_DUMP_FILE):
    with open(FILTERED_DUMP_FILE) as file:
        messages = utils.byteify(json.load(file, encoding='utf-8'))
else:
    messages = extract_messages.extract(RAW_DATA_PATH, SELF_NAME)
    extract_messages.dump(FILTERED_DUMP_FILE)

lines = []
f_train = open(FASTTEXT_TRAIN_FILE, 'w')
f_test = open(FASTTEXT_TEST_FILE, 'w')
f_validation = open(FASTTEXT_TEST_VALIDATION_FILE, 'w')

for key in messages:
    for msg in messages[key]:
        lines.append('__label__' + key +  ' ' + msg.replace('\n', ' ') + '\n')

random.shuffle(lines)

lines_train = lines[:-5000]
lines_test = [' '.join(l.split()[1:]) for l in lines[-5000:]]
lines_validation = [l.split()[0] for l in lines[-5000:]]

for l in lines_train:
    f_train.write(l)
for l in lines_test:
    f_test.write(l + '\n')
for l in lines_validation:
    f_validation.write(l + '\n')

f_train.close()
f_test.close()
f_validation.close()