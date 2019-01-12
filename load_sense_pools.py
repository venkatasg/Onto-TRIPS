import os
import xml.etree.ElementTree as ET
from nltk.corpus import wordnet as wn
import index2id

smaps = '../sensemap'

nouns, verbs = index2id.read_map(smaps)

lookup = {'n': nouns, 'v': verbs}

total, found, unchanged, lost = 0, 0, 0, 0


def read_file(fname):
    global total, found, unchanged, lost
    # print(fname)
    tree = ET.parse(fname)
    sp = tree.getroot()

    name = sp.attrib['NAME']
    definition = sp.attrib['SPID']
    senses = []
    subs = []
    for sense in sp.findall("SENSE"):
        for sid in sense.findall("SENSEID"):
            w, l, c, p, i = sid.text.split(".")
            if len(i) == 1:
                i = "0" + i
            s21 = ".".join([w, p, i])
            total += 1
            try:
                if wn.synset(s21):
                    unchanged += 1
            except:
                pass
            if s21 in lookup[p]:
                found += 1
                s, v = lookup[p][s21]
                if s != s21:
                    pass
                    # print("mapping", s21, "to", v)
                for x in v:
                    senses.append((s, wn.synset(x)))
            else:
                lost += 1
                pass
                # print("sense not found:", s21)
    for subto in sp.findall("SUBTO"):
        for subtag in subto.findall("SUBTAG"):
            subs.append(subtag.text)
    return name, senses, definition, subs


def upperont(fname):
    tree = ET.parse(fname)
    top = tree.getroot()
    uo = []

    for sp in top.findall("SENSEPOOL"):
        st = []
        for sbto in sp.findall("SUBTO"):
            st += [st.text for st in sbto.findall("SUBTAG")]
        uo.append((sp.attrib['NAME'], st))
    return uo


def read_all(folder):
    res = []
    for filename in os.listdir(folder+"/sense-pools"):
        if filename.endswith("xml"):
            res.append(read_file(folder+"/sense-pools/"+filename))
    
    print("Total:", total, "Found:", found, "Unchanged:", unchanged, "Lost:", lost)
    return res, upperont(folder+"/upper-model.xml")



