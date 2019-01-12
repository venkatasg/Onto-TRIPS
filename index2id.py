#import os

int2pos = {
        1: 'n',
        2: 'v',
        3: 'a',
        4: 'r',
        5: 's'
        }

def pmono(line, pos):
    l21, off21, l30, off30 = line.split()
    name21 = ".".join([l21.split("%")[0], pos, "01"])
    name30 = ".".join([l30.split("%")[0], pos, "01"])
    return name21, [name30], 100

def monofile(fname, pos):
    f = open(fname)
    return [pmono(line, pos) for line in f.readlines()]

def extractsc(info, pos):
    l = info.split("%")[0]
    num = info.split(";")[-1]
    if len(num) == 1:
        num = "0" + num
    return ".".join([l, pos, num])

def ppoly(line, pos):
    line = line.split()
    info_21 = line[1]
    info_30 = line[2:]
    info_21 = extractsc(info_21, pos)
    info_30 = [extractsc(i, pos) for i in info_30]
    return info_21, info_30, int(line[0])

def polyfile(fname, pos):
    f = open(fname)
    return [ppoly(line, pos) for line in f.readlines()]

def read_map(mapdir, frm="2.1", to="3.0"):
    def fname(t, p):
        return "".join([mapdir, "/", frm, "to", to, ".", p, ".", t])

    nmono = monofile(fname("mono", "noun"), 'n')
    vmono = monofile(fname("mono", "verb"), 'v')

    npoly = polyfile(fname("poly", "noun"), 'n')
    vpoly = polyfile(fname("poly", "verb"), 'v')

    nouns = {k: (s, v) for k, v, s in nmono+npoly}
    verbs = {k: (s, v) for k, v, s in vmono+vpoly}

    return nouns, verbs
