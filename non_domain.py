#!/usr/bin/env python

from input_data import InputData
from normalizer import Tokenizer, Stemmer
from spell_correct import SpellReplacer
from os import walk

class NonDomainClassfier(object):
    def __init__(self):
        self.wordDict = {}
        self.spellReplacer = SpellReplacer()
        self.tokenizer = Tokenizer()
        self.stemmer = Stemmer()

    def train(self, eachDict):
        for each_ans in eachDict['otherStudentAnswers']:
            if each_ans['accuracy'] == 'non_domain':
                self.add_dict(each_ans['text'])

    def add_dict(self, text):
        for raw_token in self.tokenizer.tokenize(text):
            token = self.spellReplacer.replace(raw_token)
            if  token != None:
                token = self.stemmer.stem(token)
                if token in self.wordDict:
                    self.wordDict[token] += 1
                else:
                    self.wordDict[token] = 1

    def check(self, text):
        tokens = []
        for raw_token in self.tokenizer.tokenize(text):
            token = self.spellReplacer.replace(raw_token)
            if  token != None:
                tokens.append(self.stemmer.stem(token))
        score = 0.0
        for token in tokens:
            if token not in self.wordDict:
                return False
        return True

    def train_all(self, dictList):
        for eachDict in dictList:
            self.train(eachDict)

if __name__ == '__main__':
    
    reader1 = InputData('seb', '../SemEval/train/seb/Core/')
    dictList1 = reader1.readDir()
    reader2 = InputData('beetle', '../SemEval/train/beetle/Core/')
    dictList2 = reader2.readDir()
    nonDomain = NonDomainClassfier()
    nonDomain.train_all(dictList1)
    nonDomain.train_all(dictList2)
    print len(nonDomain.wordDict)

