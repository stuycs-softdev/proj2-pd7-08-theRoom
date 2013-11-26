from random import choice
# our magical, automated reviewer


def weightedListofKeys(corpus):
    out = []
    for key in corpus:
        for i in range(corpus[key]):
            out.append(key)
    return out

# returns a list of keys, with there being weight instances of each key
def weightedListofKeys2D(corpus):
    out = []
    for key in corpus:
        for k in corpus[key]:
            for i in range(corpus[key][k]):
                out.append(key)
    return out


from collections import defaultdict
from re import sub, UNICODE

START = -1
END = -2
# credit to Earwig for this (I got his permission to use it)
# https://github.com/earwig/earwigbot/blob/develop/earwigbot/wiki/copyvios/markov.py
def generateCorpus(text):
    """Implements a basic ngram Markov chain of words."""
    degree = 3  # 2 for bigrams, 3 for trigrams, etc.
    chain = defaultdict(lambda: defaultdict(lambda: 0))
    words = sub("", "", text.lower(), flags=UNICODE).split()
    padding = degree - 1
    words = ([START] * padding) + words + ([END] * padding)
    for i in range(len(words) - degree + 1):
        last = i + degree - 1
        chain[tuple(words[i:last])][words[last]] += 1
    return chain


def generateSentence(corpus):
    pick = choice(weightedListofKeys2D(corpus))
    sentence = str(pick[0]) + " "
    while not END in pick:
        sentence += str(pick[1]) + " " 
        pick = (pick[1], choice(weightedListofKeys(corpus[pick])))
    return sentence

def generateSentenceWithGrammar(corpus):
    max_len = 20
    sentence = generateSentence(corpus)
    while len(sentence.split(' ')) > max_len:
        sentence = generateSentence(corpus)
    return sentence

corpus = generateCorpus("the quick brown fox jumps over the lazy dog really quickly because he is a quick brown fox jumping over the lazy dog.")

print generateSentenceWithGrammar(corpus)
