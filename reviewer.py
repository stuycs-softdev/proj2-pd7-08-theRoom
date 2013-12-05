from random import choice
from document import doc
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

START = doc.SQLss
END = doc.SQLes
# credit to Earwig for this (I got his permission to use it)
# https://github.com/earwig/earwigbot/blob/develop/earwigbot/wiki/copyvios/markov.py
def generateCorpus(text, corpus=None):
    """Implements a basic ngram Markov chain of words."""
    degree = 3  # 2 for bigrams, 3 for trigrams, etc.
    sentences = text.split(". ")
    if (len(sentences) > 1):
        for sentence in sentences:
            corpus = generateCorpus(sentence, corpus)
        return corpus
    # use the given corpus, else use a blank new one.
    chain = defaultdict(lambda: defaultdict(lambda: 0)) if corpus == None else corpus
    words = sub("", "", text.lower(), flags=UNICODE).split()
    padding = degree - 1
    words = ([START] * padding) + words + ([END] * padding)
    for i in range(len(words) - degree + 1):
        last = i + degree - 1
        chain[tuple(words[i:last])][words[last]] += 1
    return chain


def generateSentence(corpus):
    pick = [END, END];
    while pick[0] != START:
        pick = choice(weightedListofKeys2D(corpus))
    sentence = " "
    while not END in pick:
        if pick[1] != START:
            sentence += str(pick[1]) + " " 
        pick = (pick[1], choice(weightedListofKeys(corpus[pick])))
    return sentence

def generateSentenceWithGrammar(corpus):
    max_len = 20
    sentence = generateSentence(corpus)
    while len(sentence.split(' ')) > max_len:
        sentence = generateSentence(corpus)
    return sentence

corpus = None
for sentence in open('quorum4').read().split('. '):
	corpus = generateCorpus(sentence + '.', corpus)

print generateSentenceWithGrammar(corpus)
