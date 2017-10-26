#! /usr/bin/env python3

from functools import reduce
import sys

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

GOLD_BIOS = []
WORDS = []
PRED_BIOS = []

def read_file(input, lst, add_words):
    with open(input, 'r') as f:
        for l in f:
            l = l.strip()
            l = l.split()
            if len(l) == 0:
                continue
            lst.append(l[0])
            if add_words:
                WORDS.append(l[1])

def process_list(l):
    in_entity = False
    entities = []
    entity = [None, None]
    last_i = 0
    etype = None
    for i in range(len(l)):
        if l[i][0] == 'B':
            if in_entity:
                entity[1] = last_i
                entities.append((etype,)+tuple(entity))
            entity = [i, None]
            etype = l[i][2]
            in_entity = True
        elif l[i][0] == 'I':
            if in_entity and l[i][2] != etype:
                entity[1] = last_i
                entities.append((etype,)+tuple(entity))
                etype = None
                in_entity = False
        else:
            if in_entity:
                entity[1] = last_i
                entities.append((etype,)+tuple(entity))
            etype = None
            in_entity = False
        last_i = i
    return entities

def run_eval():
    frac = lambda x,y: str(x) + '/' + str(y) if y != 0 else 'n/a'
    predict = sys.argv[1]
    gold = sys.argv[2]
    read_file(gold, GOLD_BIOS, True)
    read_file(predict, PRED_BIOS, False)
    assert(len(GOLD_BIOS) == len(PRED_BIOS))
    gold_ents = process_list(GOLD_BIOS)
    pred_ents = process_list(PRED_BIOS)
    
    gold_locs = [x for x in gold_ents if x[0] == 'L']
    gold_pers = [x for x in gold_ents if x[0] == 'P']
    gold_orgs = [x for x in gold_ents if x[0] == 'O']

    pred_locs = [x for x in pred_ents if x[0] == 'L']
    pred_pers = [x for x in pred_ents if x[0] == 'P']
    pred_orgs = [x for x in pred_ents if x[0] == 'O']

    correct_locs = [x for x in pred_locs if x in gold_locs]
    correct_pers = [x for x in pred_pers if x in gold_pers]
    correct_orgs = [x for x in pred_orgs if x in gold_orgs]

    print(
'''Correct PER = {}
Recall PER = {}
Precision PER = {}

Correct LOC = {}
Recall LOC = {}
Precision LOC = {}

Correct ORG = {}
Recall ORG = {}
Precision ORG = {}

Average Recall = {}
Average Precision = {}'''.format(
    " | ".join([" ".join(WORDS[x[1]:x[2]+1])+" ["+str(x[1]+1)+"-"+str(x[2]+1)+']' for x in correct_pers]) if len(correct_pers) != 0 else "NONE",
    frac(len(correct_pers), len(gold_pers)),
    frac(len(correct_pers), len(pred_pers)),
    " | ".join([" ".join(WORDS[x[1]:x[2]+1])+" ["+str(x[1]+1)+"-"+str(x[2]+1)+']' for x in correct_locs]) if len(correct_locs) != 0 else "NONE",
    frac(len(correct_locs), len(gold_locs)),
    frac(len(correct_locs), len(pred_locs)),
    " | ".join([" ".join(WORDS[x[1]:x[2]+1])+" ["+str(x[1]+1)+"-"+str(x[2]+1)+']' for x in correct_orgs]) if len(correct_orgs) != 0 else "NONE",
    frac(len(correct_orgs), len(gold_orgs)),
    frac(len(correct_orgs), len(pred_orgs)),
    frac(len(correct_pers) + len(correct_locs) + len(correct_orgs),
         len(gold_pers) + len(gold_locs) + len(gold_orgs)),
    frac(len(correct_pers) + len(correct_locs) + len(correct_orgs),
         len(pred_pers) + len(pred_locs) + len(pred_orgs))))
    
    
if __name__ == '__main__':
    run_eval()
