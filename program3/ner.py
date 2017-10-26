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

def to_feature_idx(dic, word_list, word, start_idx):
    if word in dic.keys():
        return dic[word] + start_idx
    try:
        idx = word_list.index(word)
    except:
        if type(word) != str:
            pass # special
        else:
            idx = len(word_list) + 1 # Unknown
    dic[word] = idx
    return idx + start_idx

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

def parse_file(input):
    with open(input, 'r') as f:
        iters = 0
        word_cons = [None, None]
        pos_cons = [None, None]
        eos = False
        bio = None
        for l in f:
            l = l.strip()
            l = l.split()
            if len(l) == 0:
                iters = 0
                if not eos:
                    yield (word_cons[0], word_cons[1], "OMEGA",
                           pos_cons[0], pos_cons[1], "OMEGAPOS",
                           is_abbr(word_cons[0]), is_cap(word_cons[0]), is_loc(word_cons[0]), bio)
                    eos = True
                continue
            assert(len(l) == 3)
            nbio, pos, w = l[0], l[1], l[2]
            if w not in WORDS:
                w = "UNK"
            if pos not in POSS:
                pos = "UNKPOS"
            if iters == 0:
                word_cons[0] = "PHI"
                pos_cons[0] = "PHIPOS"
            #print(word_cons, pos_cons, w, pos)
            if iters > 0:
                yield (word_cons[0], word_cons[1], w,
                       pos_cons[0], pos_cons[1], pos,
                       is_abbr(word_cons[0]), is_cap(word_cons[0]), is_loc(word_cons[0]), bio)
            bio = nbio
            iters += 1
            word_cons[1], pos_cons[1] = word_cons[0], pos_cons[0]
            word_cons[0], pos_cons[0] = w, pos
            eos = False

# to_feature_idx(dic, word_list, word, start_idx):
def produce_vecs(input, opt, word_list, word_dict, pos_list, pos_dict, fout):
    for i in parse_file(input):
        result = []
        w, w_prev, w_next, pos, pos_prev, pos_next, abbr, cap, loc, lab = i
        if opt.word:
            result.append(to_feature_idx(word_dict, word_list, w, opt.word_idx))
        if opt.wordcon:
            result.append(to_feature_idx(word_dict, word_list, w_next, opt.word_next_idx))
            result.append(to_feature_idx(word_dict, word_list, w_prev, opt.word_prev_idx))
        if opt.pos:
            result.append(to_feature_idx(pos_dict, pos_list, pos, opt.pos_idx))
        if opt.poscon:
            result.append(to_feature_idx(pos_dict, pos_list, pos_next, opt.pos_next_idx))
            result.append(to_feature_idx(pos_dict, pos_list, pos_prev, opt.pos_prev_idx))
        if opt.abbr and abbr:
            result.append(opt.abbr_idx)
        if opt.cap and cap:
            result.append(opt.cap_idx)
        if opt.locs and loc:
            result.append(opt.loc_idx)
#        print(i)
        print(str(labelings[lab]) + " " + " ".join(list(map(lambda x: str(x) + ":1", sorted(result)))))
            

def read_locs(opt):
    with open(opt.locs, 'r') as f:
        for loc in f:
            LOCS.add(loc.strip())

def yes_no(b):
    if b:
        return "yes"
    return "no"
            
def produce_readable(input, opt, fout):
    na = lambda x,y: (x if y else "n/a")
    for i in parse_file(input):
        w, w_prev, w_next, pos, pos_prev, pos_next, abbr, cap, loc, lab = i
        print(
'''WORD: {}
WORDCON: {}
POS: {}
POSCON: {}
ABBR: {}
CAP: {}
LOCATION: {}\n'''.format(na(w, opt.word), na(w_prev+" "+w_next, opt.wordcon),
                         na(pos, opt.pos), na(pos_prev+" "+pos_next, opt.poscon),
                         na(yes_no(abbr), opt.abbr),
                         na(yes_no(cap), opt.cap),
                         na(yes_no(loc), opt.location)), file=fout)
            
def run_ner():
    opt = process_args()
    read_locs(opt)
    preprocess(opt.train, opt)
    word_list = list(WORDS)
    pos_list = list(POSS)
    word_dict = dict()
    pos_dict = dict()
    
    opt.word_idx = 1
    opt.word_next_idx = opt.word_idx + len(word_list) + 3 # OMEGA + UNK
    opt.word_prev_idx = opt.word_next_idx + len(word_list) + 3 # PHI + UNK
    opt.pos_idx = opt.word_prev_idx + len(word_list) + 3 # UNK
    opt.pos_next_idx = opt.pos_idx + len(pos_list) + 3 # UNK + OMEGAPOS
    opt.pos_prev_idx = opt.pos_next_idx + len(pos_list) + 3 # UNK + PHIPOS
    opt.abbr_idx = opt.pos_prev_idx + len(pos_list) + 2
    opt.cap_idx = opt.abbr_idx + 2
    opt.loc_idx = opt.cap_idx + 2
    
    
    #produce_readable(opt.train, opt, sys.stdout)
    produce_vecs(opt.train, opt, word_list, word_dict, pos_list, pos_dict, sys.stdout)
    
    
if __name__ == '__main__':
    run_ner()
