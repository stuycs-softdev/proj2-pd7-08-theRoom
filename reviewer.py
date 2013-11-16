from random import choice
# our magical, automated reviewer


# corpuses
#{
    #'first': {
        #'weight1':thing,
        #'weight2':thing, 
        #'second': {
            #'weight1':thing,
            #'third': {
                #bunch of weights
                #}
            #}
        #}
#}


# returns a list of keys, with there being weight instances of each key
def weightedListofKeys(corpus):
    out = []
    for key in corpus:
        for k in corpus[key]:
            for i in range(corpus[key][k]):
                out.append(key)
    return out


from collections import defaultdict
from re import sub, UNICODE

# credit to Earwig for this (I got his permission to use it)
# https://github.com/earwig/earwigbot/blob/develop/earwigbot/wiki/copyvios/markov.py
def generateCorpus(text):
    """Implements a basic ngram Markov chain of words."""
    START = -1
    END = -2
    degree = 3  # 2 for bigrams, 3 for trigrams, etc.
    chain = defaultdict(lambda: defaultdict(lambda: 0))
    words = sub("[^\w\s-]", "", text.lower(), flags=UNICODE).split()
    padding = degree - 1
    words = ([START] * padding) + words + ([END] * padding)
    for i in range(len(words) - degree + 1):
        last = i + degree - 1
        chain[tuple(words[i:last])][words[last]] += 1
    return chain


corpus = generateCorpus("the quick the quick the quick the quick the quick")
for key in corpus:
    print key,':',corpus[key]

print "---"
print weightedListofKeys(corpus)
