#! /usr/bin/env python3

from functools import reduce
import sys

WORD_DICT = set()
POS_DICT  = set()
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
    pass

def produce_vecs(input, opt, unk):
    pass

def read_locs(opt):
    with open(opt.locs, 'r') as f:
        for loc in f:
            LOCS.add(loc)
        

def run_ner():
    opt = process_args()
    read_locs(opt)
    preprocess(opt.train, opt)
    produce_vecs(opt.train, opt, False)
    
if __name__ == '__main__':
    run_ner()
    print(LOCS)
