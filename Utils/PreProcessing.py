from processors import *
import numpy as np

"""
Currently not using preprocessing methods available in keras.  Using pyprocessors [https://github.com/myedibleenso/py-processors]
"""

#initialize a processor
def initializeProcessor():
    return Processor(port=8886)


#start server
def startServer(proc):
    proc.start_server(jar_path="processors-server.jar")


#annotate text
def annotate(proc, text):
    return proc.annotate(text)


"""
other methods
"""

#sort sequences by length
def sortBySeqLength(seqs):
    #instantiate empty dictionary
    dict = {}

    for s in seqs:
        #get length
        length = len(s)
        #if length alreayd in keys
        if length in dict.keys():
            #append this seq to list
            dict[length].append(s)
        else:
            #add key and this sequence as first item
            dict[length] = [s]

    return dict


#pad to longest sequence length
def padToLongest(dictOfSeqs):
    #get lengths from dictionary
    keys = dictOfSeqs.keys()
    #get longest length
    longest = max(keys)
    #iterate through dictionary keys and pad
    new_dict = {}
    for k in keys:
        if k != longest:
            seqs = dictOfSeqs[k]
            padded_seqs = []
            for s in seqs:
                #pad with 0s at the end til it's the same length as longest sequence
                padded_s = np.pad(s, pad_width=(0,longest-k), mode="constant")
                #add to padded_seqs
                padded_seqs.append(padded_s)
            #add to new dictionary
            new_dict[k] = padded_seqs
        else:
            new_dict[k] = dictOfSeqs[k]

    return new_dict


#get word vector
def getVector(word, gensimModel, w2vDim):
    if word in gensimModel:
        return gensimModel[word]
    else:
        return np.zeros(w2vDim)


def convertSentenceToVec(listOfWords, gensimModel, w2vDim):
    return [getVector(word, gensimModel, w2vDim) for word in listOfWords]





