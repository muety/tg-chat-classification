# Execute this right from within the directory the file is stored in

from __future__ import division
from datetime import datetime
import subprocess
import fasttext_preprocess

FASTTEXT_PATH = './../fastText/'

def fasttext_train():
    cmd = FASTTEXT_PATH + 'fasttext supervised -input ' + fasttext_preprocess.FASTTEXT_TRAIN_FILE + ' -output ' + FASTTEXT_PATH + 'model'
    # print 'Executing: ' + cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    streamdata = p.communicate()[0]
    print 'Training successful' if p.returncode == 0 else 'There was an error while training: ' + str(p.returncode)
    return p.returncode == 0

def fasttext_test():
    cmd = FASTTEXT_PATH + 'fasttext predict ' + FASTTEXT_PATH + 'model.bin ' + fasttext_preprocess.FASTTEXT_TEST_FILE
    lines = []
    # print 'Executing: ' + cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        lines.append(line)
    streamdata = p.communicate()[0]
    if p.returncode == 0: 'There was an error while testing: ' + str(p.returncode)
    return lines if p.returncode == 0 else False

f_validation = open(fasttext_preprocess.FASTTEXT_TEST_VALIDATION_FILE, 'r')
labels = f_validation.readlines()

print 'Training fasttext...'
start = datetime.now()
fasttext_train()
print 'Training time: ' + str((datetime.now() - start).total_seconds()) + ' s'

print 'Testing with fasttext...'
start = datetime.now()
lines = fasttext_test()

c = 0
for i, val in enumerate(lines):
    if val == labels[i]: c += 1

print 'Testing time: ' + str((datetime.now() - start).total_seconds()) + ' s'

print '----'
print 'Tested messages: ' + str(len(lines))
print 'Accuracy: ' + str(c / len(lines))

f_validation.close()