#!/usr/bin/env python2.7

from os import listdir
from input_data import InputData
import plsa
from WordNetSimilarity import WordnetSimilarity
from normalizer import Tokenizer
#from output import output
#import parsers

tokenizer = Tokenizer()

class plsaModeler(object):
    def __init__(self, dataset_type, path):
        """
            dataset_type: "beetle" or "seb"
            path: the path of test data
            mode: 2, 3 or 5
            output_filename: "filename"
        """
        self.modes={
                2: [0.75],
                3: [0.40, 0.75],
                5: [0.1, 0.15, 0.20, 0.30]
                }
        self.dataset_type = dataset_type
        self.path = path
        self.model={}
        self.ws=WordnetSimilarity()


    def train(self):
        rsl = []
        files = listdir(self.path)
        reader = InputData(self.dataset_type, self.path)
        corpus = plsa.Corpus()
        for filename in files:
            vectors=[]
            question = reader.readFile(filename)
            id = question["id"]
            for r in question["referenceAnswers"]:
                rid=r["id"]
                references=[ sr["text"] for sr in r["studentAnswers"]]
                """
                for ans in question["student_answers"]:
                    if ans["id"]==rid:
                        references.append(ans["text"])
                #references=[ self.stemmer.stem(sr["text"]) for sr in r["studentAnswers"]]
                """
                references.append(r["text"])
                corpus.addBaseline(references)
                #print corpus.getVector()
                vectors.append(corpus.getVector())
                corpus.reset()

            self.model[id]=vectors

        return

    def grade(self,qid,answer):
        max_score=0.0
        print self.model[qid]
        for vector in self.model[qid]:
            score=self.ws.getScore(self.ws.getSimilarityMatrix(vector[0],tokenizer.tokenize(answer)),vector[1])
            if score>max_score:
                max_score=score

        return max_score


if __name__ == "__main__":
    basci = plsaModeler("beetle", "../SemEval/train/beetle/Core/")
    basci.train()
    print basci.grade("BULB_C_VOLTAGE_EXPLAIN_WHY1","Terminal 1 and the positive terminal are separated by the gap")
    print basci.grade("BULB_C_VOLTAGE_EXPLAIN_WHY1","positive battery terminal is separated by a gap from terminal 1")
    print basci.grade("BULB_C_VOLTAGE_EXPLAIN_WHY1","the terminals are seperated")
    print basci.grade("BULB_C_VOLTAGE_EXPLAIN_WHY1","Voltage is the difference between a positive and negative end on a battery.")
    #print basci.model


