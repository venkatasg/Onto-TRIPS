from os.path import expanduser
import pickle
from utility import get_senses, get_types
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from genesis.tools.trips import ontology as ont
import random
from tqdm import tqdm

home = expanduser('~')


def remove_useless(sentences, senses):
    indices = [i for i, x in enumerate([all((a[:2] == '--') for a in senses[i]) for i in range(len(senses))]) if not x]
    sentences = [sentences[i] for i in indices]
    senses = [senses[i] for i in indices]
    available_senses = list(set([a for sense in senses for a in sense if a[0:2] != '--']))
    return sentences, senses, available_senses


if __name__ == '__main__':
    with open(home + '/Downloads/conll-formatted-ontonotes-5.0/train.pkl', 'rb') as f_train, open(home + '/Downloads/conll-formatted-ontonotes-5.0/dev.pkl', 'rb') as f_dev, open(home + '/Downloads/conll-formatted-ontonotes-5.0/test.pkl', 'rb') as f_test:
        sentences, senses = pickle.load(f_train)
        dev_sents, dev_senses = pickle.load(f_dev)
        test_sents, test_senses = pickle.load(f_test)

    sentences, senses, available_senses = remove_useless(sentences, senses)
    dev_sents, dev_senses, _ = remove_useless(dev_sents, dev_senses)
    test_sents, test_senses, _ = remove_useless(test_sents, test_senses)

    ont_senses = [a for a in get_senses() if a.group == '1']
    trips_names = [a.name for a in list(ont.data.values())]

    sense_names = [(x.lemma + '-' + x.pos + '-' + str(x.num)) for x in ont_senses]
    sense_names_mod = [a for a in sense_names if a in available_senses]
    baseline_map = pd.DataFrame(0, index=sense_names_mod, columns=trips_names)

    sense_dict = defaultdict(None, {(x.lemma + '-' + x.pos + '-' + str(x.num)): x for x in ont_senses})
    for sent, sense in tqdm(zip(sentences, senses), total=len(sentences)):
        for s_name in sense:
            if sense_dict.get(s_name):
                for maps in sense_dict.get(s_name).mappings:
                    for t_type in maps.maps_to():
                        t_name = t_type.name
                        baseline_map.loc[s_name][t_name] += 1

    baseline_map = baseline_map[(baseline_map.T != 0).any()]
    # print max value as map
    outputs = []

    rands = random.sample(range(len(dev_sents) - 1), 100)
    dev_sents_ = [dev_sents[i] for i in rands]
    dev_senses_ = [dev_senses[i] for i in rands]

    for sent, sense in tqdm(zip(dev_sents, dev_senses), total=len(dev_sents)):
        input_sent = " ".join(sent)
        output_sent = []
        for s_name in sense:
            if s_name in baseline_map.index:
                t_name = baseline_map.idxmax(axis=1).loc[s_name]
                output_sent.append(t_name)
            else:
                output_sent.append('_')
        outputs.append((input_sent, " ".join(sense), " ".join(output_sent)))

    df = pd.DataFrame(outputs, columns=["Sentence", "Senses", "TRIPS"])
    df.to_csv('all-mappings.tsv', sep='\t', index=False)
