# /usr/bin/env python3

from gramify import to_unigrams
from gramify import to_bigrams
import math
from pprint import pprint


unigram_freqs = dict()
unigram_count = 0

# Maps w_{n-1} to w_n and ("count")
bigram_freqs = dict()
bigrams_seen = 0

def bigram_created():
    global bigrams_seen
    bigrams_seen += 1
    return 0

def bigram_logprob(b):
    if (b[0] not in bigram_freqs.keys() and
        b[1] not in bigram_freqs[b[0]].keys()):
        raise Exception()
    
    f = bigram_freqs[b[0]][b[1]]
    if b[0] is None:
        den = bigram_freqs[None][("count",)]

    else:
        den = unigram_freqs[b[0]]       
    return math.log(f/den,2)

def to_bigram_logprob(s):
    try:
        s = math.fsum(map(lambda x: bigram_logprob(x), to_bigrams(s)));
    except:
        return "undefined"
    return "{:0.4f}".format(s)

def unigram_logprob(u):
    return math.log(unigram_freqs[u]/unigram_count, 2)

def to_unigram_logprob(s):
    s = math.fsum(map(lambda x: unigram_logprob(x), to_unigrams(s)));
    return "{:0.4f}".format(s)

with open("train.txt", 'r') as f:
    for l in f:
        # Unigrams
        for u in to_unigrams(l):
            unigram_freqs[u] = unigram_freqs.get(u, 0) + 1
            unigram_count += 1
        
        # Bigrams
        for u in to_bigrams(l):
            w_n1, w_n = u
            if w_n1 not in bigram_freqs.keys():
                bigram_freqs[w_n1] = {("count",) : 0}
            bigram_freqs[w_n1][("count",)] += 1
            bigram_freqs[w_n1][w_n] = bigram_freqs[w_n1].get(w_n, bigram_created()) + 1

num_unigrams = len(unigram_freqs.keys())
potential_bigrams = (num_unigrams+1)*num_unigrams
with open("test.txt") as f:
    for s in f:
        s = s.strip()
        print('''S = {}

Unsmoothed Unigrams, logprob(S) = {}
Unsmoothed Bigrams, logprob(S) = {}
'''.format(s,
           to_unigram_logprob(s),
           to_bigram_logprob(s)))

