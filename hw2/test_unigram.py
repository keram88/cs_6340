from gramify import to_unigrams
import math

freqs = dict()

count = 0

with open("train.txt", 'r') as f:
    count = 0
    for l in f:
        for u in to_unigrams(l):
            freqs[u] = freqs.get(u, 0) + 1
            count += 1

p=math.fsum(map(lambda x: math.log(freqs[x.lower()]/count, 2), "But old Mr. Toad will leave one day . ".split()))
            
print("{:0.4f}".format(p))
