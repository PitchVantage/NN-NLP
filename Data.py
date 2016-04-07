import Utils.PreProcessing as pre

class Data():

    def __init__(self, filepath, lineSeparated=False):
        self.filepath = filepath
        self.lineSeparated = lineSeparated
        self.p = None
        self.lines = None
        self.rawSents = []
        self.seqWords = []
        self.seqLemmas = []


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


    def getTokenizedWords(self):
        self.seqWords = [self.rawSents[i].words for i in range(len(self.rawSents))]


    def getTokenizedLemmas(self):
        self.seqLemmas = [self.rawSents[i].lemmas for i in range(len(self.rawSents))]
