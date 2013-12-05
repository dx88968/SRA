#!/usr/bin/env python2.7

class IrrelevantDetector:
    def __init__(self):
        self.model=set()

    def build(self,references):
        for ref in references:
            for word in ref:
                self.model.add(word)

    def isIrrelevent(self,sentence):
        count=0
        for word in sentence:
            if word in self.model:
                count=count+1

        score=float(count)/float(len(self.model))
        if score<0.1:
            return True
        else:
            return False
