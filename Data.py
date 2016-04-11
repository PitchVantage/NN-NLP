import Utils.PreProcessing as pre
import re
import itertools


class Data():

    def __init__(self, filepath, lineSeparated=False, filterPunctuation=True, lowerCase=True):
        self.filepath = filepath
        self.lineSeparated = lineSeparated
        self.filterPunctuation = filterPunctuation
        self.lowerCase = lowerCase
        self.p = None
        self.rawSents = []
        self.seqWords = []
        self.seqLemmas = []
        self.vocWordToIDX = {}
        self.vocLemmaToIDX = {}
        self.vocIDXtoWord = {}
        self.vocIDXtoLemma = {}


    def startServer(self):
        self.p = pre.initializeProcessor()
        pre.startServer(self.p)


    def stopServer(self):
        self.p.__del__()


    def annotateText(self):
        #if already one sentence per line
        if self.lineSeparated:
            #open file
            f = open(self.filepath, "rb")

            #iterate through lines
            for line in f:
                #strip \n
                clean = line.rstrip()
                #annotate
                annotated = pre.annotate(self.p, clean)
                #add to list of lines
                self.rawSents.append(annotated)
        #if not one sentence per line
        else:
            #open
            f = open(self.filepath, "rb")

            #iterate through lines
            for line in f:
                #strip \n
                clean = line.rstrip()
                #annotate entire line
                annotated = pre.annotate(self.p, clean)
                #separate into sentences
                sentences = annotated.sentences
                #add each sentence to list of lines
                for sent in sentences:
                    self.rawSents.append(sent)

        f.close()


    #filter punctuation as iterating
    def getTokenized(self):
        cWord = 0
        cLemma = 0
        #add sentences to list and words to vocabulary
        for sent in self.rawSents:
            #list to house sentences of words
            sentWordBuffer = []
            #list to house sentences of lemmas
            sentLemmaBuffer = []
            #isolate the words
            words = sent.words
            #isolate the lemmas
            lemmas = sent.lemmas
            #iterate through each word
            for i in range(len(sent.words)):
                word = words[i]
                lemma = lemmas[i]
                #if converting to lower case
                if self.lowerCase:
                    #add the word to the sentence buffer
                    sentWordBuffer.append(word.lower())
                    #build indices
                    if word.lower() not in self.vocWordToIDX:
                        cWord += 1
                        self.vocWordToIDX[word.lower()] = cWord
                        self.vocIDXtoWord[cWord] = word.lower()
                else:
                    #add the word to the sentence buffer
                    sentWordBuffer.append(word)
                    #build indices
                    if word not in self.vocWordToIDX:
                        cWord += 1
                        self.vocWordToIDX[word] = cWord
                        self.vocIDXtoWord[cWord] = word
                #add to sentence buffer
                sentLemmaBuffer.append(lemma.lower())
                #build indices
                if lemma not in self.vocLemmaToIDX:
                    cLemma += 1
                    self.vocLemmaToIDX[lemma] = cLemma
                    self.vocIDXtoLemma[cLemma] = lemma
            self.seqWords.append(sentWordBuffer)
            self.seqLemmas.append(sentLemmaBuffer)

        #filter punctuation
        if self.filterPunctuation:
            regex = '[^A-z0-9\']'
            self.seqWords = [list(itertools.ifilter(lambda x: not re.match(regex, x) and x != "'", self.seqWords[i])) for i in range(len(self.seqWords))]
            self.seqLemmas = [list(itertools.ifilter(lambda x: not re.match(regex, x) and x != "'", self.seqLemmas[i])) for i in range(len(self.seqLemmas))]



