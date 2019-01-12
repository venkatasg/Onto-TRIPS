import os
from collections import defaultdict as ddict, Counter
import xml.etree.ElementTree as ET
from nltk.corpus import wordnet as wn
from genesis.tools.trips import ontology as ont

class Ontonotes:
    def __init__(self, nodes):
        self.data = {}
        for n in nodes:
            self.data[n.name] = n
        for n in nodes:
            n.ancestors = [self.data.get(a, a) for a in n.ancestors]
            for a in n.ancestors:
                if type(a) is str:
                    print(n.name, "->",a)
                else:
                    a.children.append(n)

    def get(self, name):
        return self.data.get(name, None)
    
    def add_si(self, si):
        """si is a dictionary of senses from the inventory"""
        for d in self.data.values():
            d.senses = [si.get(a, a) for a in d.senses]

class OntoNode:
    def __init__(self, fid, name, description, senses, ancestors):
        self.fid = fid
        self.name = name
        if len(self.name) == 0:
            self.name = self.fid
        self.description = description
        self.senses = senses
        self.ancestors = ancestors
        self.children = []
    
    def __str__(self):
        return "m::{}".format(self.name)
    
    def __repr__(self):
        return str(self)+"/{}".format(self.name)
    
    def __hash__(self):
        return hash(str(self))
    
    def maps_to(self, ex=True, counts=False, deep=False, cutoff=0):
        '''
        ex: whether the mapping set is combined using intersection or union
        counts: requires union.  Returns the number of subsenses map to each type
        deep: requires counts.  Counts on the wn level instead of subsense
        '''
        if not ex and counts:
            if deep:
                r = sum([m.maps_to(counts=True) for m in self.senses if type(m) is not str], Counter())
            else:
                r_ = [m.maps_to(as_set=True) for m in self.senses if type(m) is not str]
                r = Counter()
                for a in r_:
                    for s in a:
                        r[s] += 1
            for x, s in list(r.items()):
                if s < cutoff:
                    del r[x]
            return r
        res = [m.maps_to(as_set=True) for m in self.senses if type(m) is not str]
        ctr = Counter()
        if not res:
            return set([])
        elif len(res) == 1:
            return res[0]
        else:
            if ex:
                return res[0].intersection(*res)
            else:
                return res[0].union(*res)   


def read_sp(sp):
    fid = sp.attrib['FID']
    name = sp.attrib['NAME']
    description = sp.attrib['SPID']
    senses = []
    subs = []
    for sense in sp.findall("SENSE"):
        for sid in sense.findall("SENSEID"):
            w,l,c,p,i = sid.text.split(".")
            if len(i) == 1:
                i = "0"+i
            senses.append(".".join([w, p, i]))
    for subto in sp.findall("SUBTO"):
        for subtag in subto.findall("SUBTAG"):
            subs.append(subtag.text)
    return OntoNode(fid, name, description, senses, subs)

def read_file(fname):
    tree = ET.parse(fname)
    sp = tree.getroot()
    return read_sp(sp)

def read_upper_ontology(fname):
    tree = ET.parse(fname)
    sp = tree.getroot()
    return [read_sp(s) for s in sp.findall("SENSEPOOL")]

def read_all(folder):
    res = []
    for filename in os.listdir(folder+"/sense-pools"):
        if filename.endswith("xml"):
            res.append(read_file(folder+"/sense-pools/"+filename))
    upper = read_upper_ontology(folder+"/"+"upper-model.xml")
    return Ontonotes(upper + res)


class WNM:
    def __init__(self, lemma, pos, num, version):
        self.version = version.strip()
        self.lemma = lemma.strip()
        self.pos = pos.strip()
        if len(num) == 1:
            num = "0"+num.strip()
        self.num = num.strip()
    
    def __str__(self):
        return ".".join([self.lemma, self.pos, self.num]) + "_" + self.version
    
    def name(self):
        return ".".join([self.lemma, self.pos, self.num])
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(str(self))
    
    def get(self):
        if self.version == "3.0":
            try:
                return wn.synset(self.name())
            except:
                return None
        else:
            return None
    
    def maps_to(self):
        s = self.get()
        if s:
            return ont.get_wordnet(self.get())
        return []
    
    def as_key(self):
        n = self.num
        if n[0] == '0':
            n = n[1:]
        return "{}.{}@{}@{}".format(self.lemma, n, self.pos, self.version)
        
class OntoSense:
    def __init__(self, lemma, pos, group, num, name, tpe, examples, mappings):
        self.lemma = lemma
        self.pos = pos
        self.group = group
        self.num = num
        self.name = name 
        self.tpe = tpe
        if type(examples) is str:
            self.examples = [e.strip() for e in examples.split("\n")]
        else:
            self.examples = examples
        
        self.mappings = mappings
    
    def strip(self):
        self.mappings = [m for m in self.mappings if m.get()]
    
    def __str__(self):
        return "/".join([self.lemma, self.pos, self.group, self.num])
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(str(self))
    
    def as_key_(self):
        n = self.num
        if len(self.num) == 1:
            n = "0"+self.num
        return "{}.{}.{}".format(self.lemma, self.pos, n)
    
    def as_key(self, sep="@"):
        return "{}{}{}{}{}".format(self.lemma, sep, self.num, sep, self.pos)
    
    def maps_to(self, as_set=False, cutoff=0, counts=False):
        x = ddict(set)
        set_w = Counter()
        for ms in self.mappings:
            m = ms.maps_to()
            x["wn"].add(ms)
            if not m:
                x["unmapped"].add(ms.name())
            for s in m:
                x[s].add(ms.name())
                set_w[ms.name()] += 1
        if as_set:
            if counts:
                return set_w
            return set([k for k in set_w.keys() if set_w[k] > cutoff])
        return x

def ssenselist(t):
    if " " in t:
        return [x.strip() for x in t.strip().split()]
    elif "," in t:
        return [x.strip() for x in t.strip().split(",")]
    else:
        return t.strip()

def process_inventory_file(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    lemma, pos = root.attrib['lemma'].rsplit("-", 1)
    senses = []
    for sense in root.findall("sense"):
        group = sense.attrib["group"]
        n = sense.attrib['n']
        name = sense.attrib['name']
        if 'type' in sense.attrib:
            tpe = sense.attrib['type']
        else:
            tpe = ""
        examples = sense.find("examples").text
        mappings = []
        for ml in sense.findall("mappings"):
            for m in ml.findall("wn"):
                l = m.attrib.get("lemma", lemma)
                v = m.attrib['version']
                if m.text:
                    mappings.extend([WNM(l, pos, x, v) for x in ssenselist(m.text)])
        senses.append(OntoSense(lemma, pos, group, n, name, tpe, examples, mappings))
    return senses

if __name__ == "__main__":
    read_all("sense-pools")
