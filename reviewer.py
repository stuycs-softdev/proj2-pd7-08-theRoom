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
        for i in range(corpus[key]['weight']):
            out.append(key)
    return out


# I should be shot for writing this code
def generateCorpus(sentence):
    words = sentence.split(' ')
    d = {}
    for i in range(len(words)):
        word = words[i]
        if word in d:
            d[word]['weight'] += 1
        else:
            d[word] = {'weight':1}
        if len(words)-1 > i:
            nextword = words[i+1]
            if nextword in d[word]:
                d[word][nextword]['weight']+=1
            else:
                d[word][nextword] = {'weight':1}
            if len(words)-2 > i:
                nextnextword = words[i+2]
                if nextnextword in d[word][nextword]:
                    d[word][nextword][nextnextword]['weight'] += 1
                else:
                    d[word][nextword][nextnextword] = {'weight':1}
    print d


generateCorpus("the quick brown fox jumps over the lazy dog")
