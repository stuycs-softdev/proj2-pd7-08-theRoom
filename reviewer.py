
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

