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
threshold=0.9

class ContradictoryClassfier:

    def __init__(self):
        return

    def isContradictory(self,references,answer):
        temp=antonymer.isNeg(answer)
        answer=temp[1]
        aflag=temp[0]
        for r in references:
            temp=antonymer.isNeg(r)
            rflag=temp[0]
            nsflag,newanswer=self.antonymReplacer(temp[1],answer)
            if nsflag:
                aflag=not aflag

            flag4=False
            if ws.getScoreWithoutWeight(ws.getSimilarityMatrix(tokenizer.tokenize(temp[1]),newanswer))>threshold:
                flag4=True

            if ((aflag!=rflag) and flag4):
                print "%s\n------------------------------------------\n%s"%(r,answer)
                return True

            if nsflag:
                aflag=not aflag

        return False


    def antonymReplacer(self,reference,answer):
        rWords=tokenizer.tokenize(reference)
        aWords=tokenizer.tokenize(answer)

        rWordSet=set([stemmer.stem(w) for w in rWords])

        flag=False
        newAnswer=[]

        for word in aWords:
            if stemmer.stem(word) in rWordSet:
                newAnswer.append(word)
                continue

            an=self.findAntonym(word,rWords)
            if an==None:
                newAnswer.append(word)
            else:
                newAnswer.append(an)
                flag=not flag

        return flag,newAnswer

    def findAntonym(self,word,targets):
        for rw in targets:
            if isantonym(word,rw):
                return rw

        return None

if __name__ == "__main__":
    c=ContradictoryClassfier()
    print c.isContradictory(["terminal 1 is not separated from the negative battery terminal"],"positive battery terminal is separated by a gap from terminal 1")