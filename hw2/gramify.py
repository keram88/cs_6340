WS = ('\t', '\n', ' ', '\r', '\v')
PUNC = ('.', '?', '!')

def to_unigrams(s):
  for u in s.strip().split():
    yield u.lower()
      

def to_bigrams(s):
  last = None
  s = s.strip().split()
  i = 0
  while i < len(s):
    u = s[i].lower()
    yield (last, u)
    if u in PUNC:
      last = None
    else:
      last = u
    i += 1
