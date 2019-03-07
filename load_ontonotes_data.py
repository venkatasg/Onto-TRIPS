import os
from os.path import expanduser
import pickle
import pandas as pd

def load_data(path, data_split):
    sentences = []
    senses = []
    ids = []
    lemmas = []
    pos = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.gold_conll'):
                with open(root + '/' + file, 'r') as f:
                    raw_data = f.read().split('\n\n')
                    del raw_data[-1]
                    ids += [[data_split + '-' + a.split()[0].replace('/', '-') + '-' + str(ind) for a in sen.split('\n') if a[0] != '#'][0] for ind, sen in enumerate(raw_data)]
                    sentences += [" ".join([a.split()[3] for a in sen.split('\n') if a[0] != '#']) for sen in raw_data]
                    lemmas += [" ".join([a.split()[6] for a in sen.split('\n') if a[0] != '#']) for sen in raw_data]
                    pos += [" ".join([a.split()[4].lower()[0] for a in sen.split('\n') if a[0] != '#']) for sen in raw_data]
                    senses += [" ".join([a.split()[8] for a in sen.split('\n') if a[0] != '#']) for sen in raw_data]
    data = pd.DataFrame({'ID': ids, 'Sentence': sentences, 'Lemma': lemmas, 'POS': pos, 'OntoSense': senses})
    data.to_csv(home + '/Downloads/conll-formatted-ontonotes-5.0/' + data_split + '.tsv', index=False, sep='\t')


home = expanduser('~')

load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/train/', 'train')
load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/test/', 'test')
load_data(home + '/Downloads/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/development/', 'dev')



