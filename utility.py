# from genesis.tools.trips import ontology as ont
# from load_sense_pools import read_all
import os
from os.path import expanduser
import numpy as np
from itertools import combinations
import json
# from collections import Counter
from load_sense_pools2 import process_inventory_file
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# hier = '../data/files/data/ontology'

# data = read_all(hier)

# data = [d for d in data if len(d[1]) > 1]

# cosine_distances = []
# for d in data[0]:
#     # print(d[2])
#     onts = []
#     for s, dx in d[1]:
#         onts += list(ont.get_wordnet(dx))
#         # print(s, dx.name(), dx.definition(), ont.get_wordnet(dx))
#     combs = combinations(onts, 2)
#     for a, b in combs:
#         cosine_distances.append(a.cosine(b))
#     # print("--")

# print(np.mean(cosine_distances), np.var(cosine_distances), np.median(cosine_distances))

# print(Counter(cosine_distances))

def get_senses():
    home = expanduser('~')
    # sensepools = []
    d = home + "/Downloads/ontonotes-release-5.0/data/files/data/english/metadata/sense-inventories/"
    res = sum([process_inventory_file(d + x) for x in os.listdir(d) if x.endswith("xml")], [])
    return res


def get_types():
    home = expanduser('~')
    d = home + "/Downloads/trips"
    ont = json.load(open(d + '/ontology.json'))
    return ont


def main():

    res = get_senses()
    len_senses = [len(a.mappings) for a in res]
    print("Mean and var of number of wn senses", np.mean(len_senses), np.var(len_senses), max(len_senses), min(len_senses))
    # plt.hist(x=len_senses)
    # plt.xlabel('Number of WN mappings')
    # plt.ylabel('Frequency')
    # plt.show()
    import ipdb; ipdb.set_trace()  # breakpoint 740842f8 //
    
    cosine_distances_inv = []
    for sinvs in res:
        ont_types = sum([list(a.maps_to()) for a in sinvs.mappings], [])
        combs = combinations(ont_types, 2)
        tmp = []
        for a, b in combs:
            tmp.append(a.cosine(b))
        if tmp:
            cosine_distances_inv.append(np.mean(tmp))
    print(np.mean(cosine_distances_inv), np.var(cosine_distances_inv), np.median(cosine_distances_inv))

    # plt.hist(x=cosine_distances_inv, bins=20)
    # plt.xlabel('Cosine distance')
    # plt.ylabel('Frequency')
    # plt.show()

# sensepools.add_si({r.as_key_(): r for r in res})


if __name__ == '__main__':
    main()
