#!/usr/bin/env python2.7

from os import listdir
from input_data import InputData
from normalizer import Tokenizer

tokenizer =Tokenizer()

class ContradictoryBigram:
    def __init__(self):
        self.model={}

    def addQuestion(self,qid,correctGroup,contractGroup):
        rbigram={}
        for ra in correctGroup:
            wordsra=tokenizer.tokenize(ra)
            for i in range(0,len(wordsra)-1):
                br=wordsra[i]+" "+wordsra[i+1]
                count=rbigram.get(br,0)
                rbigram[br]=count+1

        wbigram={}
        for wa in contractGroup:
            wordswa=tokenizer.tokenize(wa)
            for i in range(0,len(wordswa)-1):
                wr=wordswa[i]+" "+wordswa[i+1]
                if not rbigram.has_key(wr):
                    count=wbigram.get(wr,0)
                    wbigram[wr]=count+1

        self.model[qid]=wbigram



    def isContradictory(self,qid,answer):
        bigram=self.model[qid]
        answer=tokenizer.tokenize(answer)
        for i in range(0,len(answer)-1):
            w=answer[i]+" "+answer[i+1]
            if bigram.has_key(w):
                return True

        return False

    def load(self,dataset_type,inputpath):
        files = listdir(inputpath)
        reader = InputData(dataset_type, inputpath)
        for filename in files:
            question = reader.readFile(filename)
            id = question["id"]
            references=[]
            for r in question["referenceAnswers"]:
                references=references+[ sr["text"] for sr in r["studentAnswers"]]
                references.append(r["text"])

            counters=[]
            for o in question["otherStudentAnswers"]:
                if o["accuracy"]=="contradictory":
                    counters.append(o["text"])

            self.addQuestion(id,references,counters)

if __name__ == '__main__':
    c=ContradictoryBigram()
    c.load('beetle','../SemEval/train/beetle/Core')
    print c.isContradictory("BULB_C_VOLTAGE_EXPLAIN_WHY1","its connected")



