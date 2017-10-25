#! /usr/bin/env python3

from functools import reduce
import sys

WORDS = set()
POSS  = set()
LOCS = set()

PUNC = {".", "!", "?"}

labelings = {"O" : 0,
             "B-PER" : 1,
             "I-PER" : 2,
             "B-LOC" : 3,
             "I-LOC" : 4,
             "B-ORG" : 5,
             "I-ORG" : 6,
}

labels = {0 : "O",
          1 : "B-PER",
          2 : "I-PER",
          3 : "B-LOC",
          4 : "I-LOC",
          5 : "B-ORG",
          6 : "I-ORG",
}

LOWER = {chr(x) for x in range(ord('a'), ord('z')+1)}
UPPER = {chr(x) for x in range(ord('A'), ord('Z')+1)}
LETS = LOWER|UPPER

class options:
    def __init__(self):
        self.train = None
        self.test = None
        self.locs = None
        self.word = False
        self.wordcon = False
        self.pos = False
        self.poscon = False
        self.abbr = False
        self.cap = False
        self.location = False

def is_abbr(w):
    return (w[-1] == '.' and
            reduce(lambda x,y: x and y,
                   map(lambda x: x in LETS or x == ".", w[:-1]), True) and
            len(w) <= 4)

def is_cap(w):
    return w[0] in UPPER

def is_loc(w):
    return w in LOCS
        
def process_args():
    opt = options()
    opt.train = sys.argv[1]
    opt.test = sys.argv[2]
    opt.locs = sys.argv[3]
    for i in sys.argv[4:]:
        if i == "WORD":
            opt.word = True
        if i == "WORDCON":
            opt.wordcon = True
        if i == "POS":
            opt.pos = True
        if i == "POSCON":
            opt.poscon = True
        if i == "ABBR":
            opt.abbr = True
        if i == "CAP":
            opt.cap = True
        if i == "LOCATION":
            opt.location = True
    return opt

def preprocess(input, opt):
    with open(input, 'r') as f:
        for l in f:
            l = l.strip()
            if len(l) == 0:
                continue
            l = l.split()
            assert(len(l) == 3)
            bio, pos, w = l[0], l[1], l[2]
            POSS.add(pos)
            WORDS.add(w)

def produce_vecs(input, opt, unk):
    pass

def read_locs(opt):
    with open(opt.locs, 'r') as f:
        for loc in f:
            LOCS.add(loc.strip())

def yes_no(b):
    if b:
        return "yes"
    return "no"
            
def produce_readable(input, opt, unk):
    with open(input, 'r') as f:
        iters = 0
        word_cons = [None, None]
        pos_cons = [None, None]
        eos = False
        for l in f:
            l = l.strip()
            l = l.split()
            if len(l) == 0:
                iters = 0
                if not eos:
                    print(
'''WORD: {}
WORDCON: {} {}
POS: {}
POSCON: {} {}
ABBR: {}
CAP: {}
LOCATION: {}\n'''.format(word_cons[0], word_cons[1], "OMEGA", pos_cons[0], pos_cons[1], "OMEGAPOS",
                       yes_no(is_abbr(word_cons[0])), yes_no(is_cap(word_cons[0])), yes_no(is_loc(word_cons[0]))))
                    eos = True
                continue
            assert(len(l) == 3)
            bio, pos, w = l[0], l[1], l[2]
            if iters == 0:
                word_cons[0] = "PHI"
                pos_cons[0] = "PHIPOS"
#            print(word_cons, pos_cons, w, pos)
            if iters > 0:
                print(
'''WORD: {}
WORDCON: {} {}
POS: {}
POSCON: {} {}
ABBR: {}
CAP: {}
LOCATION: {}\n'''.format(word_cons[0], word_cons[1], w, pos_cons[0], pos_cons[1], pos,
                       yes_no(is_abbr(word_cons[0])), yes_no(is_cap(word_cons[0])), yes_no(is_loc(word_cons[0]))))
            iters += 1
            word_cons[1], pos_cons[1] = word_cons[0], pos_cons[0]
            word_cons[0], pos_cons[0] = w, pos
            eos = False
            
def run_ner():
    opt = process_args()
    read_locs(opt)
    preprocess(opt.train, opt)
    produce_vecs(opt.train, opt, False)
    produce_readable(opt.train, opt, False)
if __name__ == '__main__':
    run_ner()
