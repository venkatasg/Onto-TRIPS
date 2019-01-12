import os
from os.path import expanduser
import pickle


def load_data(path):
    sentences = []
    senses = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.gold_conll'):
                with open(root + '/' + file, 'r') as f:
                    xl = f.read().split('\n\n')
                    del xl[-1]
                    sentences += [[a.split()[3] for a in sen.split('\n') if a[0] != '#'] for sen in xl]
                    senses += [[(a.split()[6] + '-' + a.split()[4].lower()[0] +'-' + a.split()[8]) for a in sen.split('\n') if a[0] != '#'] for sen in xl]
    return sentences, senses


home = expanduser('~')

train_sentences, train_senses = load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/train/')
test_sentences, test_senses = load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/test/')
dev_sentences, dev_senses = load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/development/')

with open(home + '/Downloads/conll-formatted-ontonotes-5.0/train.pkl', 'wb') as f_train, open(home + '/Downloads/conll-formatted-ontonotes-5.0/dev.pkl', 'wb') as f_dev, open(home + '/Downloads/conll-formatted-ontonotes-5.0/test.pkl', 'wb') as f_test:
    pickle.dump((train_sentences, train_senses), f_train)
    pickle.dump((dev_sentences, dev_senses), f_dev)
    pickle.dump((test_sentences, test_senses), f_test)
