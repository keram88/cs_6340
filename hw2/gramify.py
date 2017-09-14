WS = ('\t', '\n', ' ', '\r', '\v')
PUNC = ('.', '?', '!')

def to_unigrams(s):
  for u in s.split():
    yield u.lower()
      


def to_bigrams(s):
  pass
