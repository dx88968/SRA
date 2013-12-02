__author__ = 'DX'

from normalizer import Tokenizer
from normalizer import Stemmer
from antonym import isantonym
from handle_antonym import HandleAntonym
from WordNetSimilarity import WordnetSimilarity

stemmer=Stemmer()
tokenizer = Tokenizer()
antonymer = HandleAntonym()
ws=WordnetSimilarity()
threshold=0.7

class ContradictoryClassfier:

    def __init__(self):
        return

    def isContradictory(self,references,answer):
        score=0.0
        temp=antonymer.isNeg(answer)
        answer=temp[1]
        aflag=temp[0]
        for r in references:
            temp=antonymer.isNeg(r)
            r=temp[1]
            rflag=temp[0]
            nsflag,newanswer=self.antonymReplacer(r,answer)
            if (aflag==rflag) != nsflag:
                if ws.getScoreWithoutWeight(ws.getSimilarityMatrix(tokenizer.tokenize(r),newanswer))>threshold:
                    return True

        return False


    def antonymReplacer(self,reference,answer):
        rWords=tokenizer.tokenize(reference)
        aWords=tokenizer.tokenize(answer)

        rWordSet=set([stemmer.stem(w) for w in rWords])

        flag=True
        newAnswer=[]

        for word in aWords:
            if stemmer.stem(word) in rWordSet:
                newAnswer.append(word)
                continue

            for rw in rWords:
                if isantonym(word,rw):
                    newAnswer.append(rw)
                    flag=not flag
                    break

        return flag,newAnswer

if __name__ == "__main__":
    c=ContradictoryClassfier()
    print c.isContradictory(["terminal 1 is connected to the negative battery terminal"],"The voltage is 1.5 because thebulb terminal is connected to the battery terminal")