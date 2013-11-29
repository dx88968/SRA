#!/usr/bin/env python2.7

from nltk.corpus import wordnet as wn
import numpy as np
import nltk

PartOfSpeech=[wn.NOUN,wn.VERB,wn.ADJ,wn.ADV,None]

class WordnetSimilarity:
    def getSimilarityMatrix(self,base,target):
        m=len(base)
        n=len(target)
        matrix=np.zeros([m, n], dtype = np.float)

        for i in range(0,m):
            for j in range(0,n):
                for POS in PartOfSpeech:
                    w1=wn.synsets(base[i], pos=POS)
                    w2=wn.synsets(target[j], pos=POS)
                    if len(w1)>0 and len(w2)>0:
                        weight = w1[0].path_similarity(w2[0])
                        if matrix[i,j]<weight:
                            matrix[i,j]=weight

        return matrix

    def applyWeight(self,matrix):
        return




    def getScore(self,matrix,weight):
        if matrix==None or len(matrix)==0 or len(matrix[0])==0:
            return 0.0
        m=len(matrix)
        n=len(matrix[0])
        sim=0.0
        maxSim_i=0.0
        maxSim_j=0.0
        sumSim_i=0.0
        sumSim_j=0.0
        for i in range(0,m):
            maxSim_i=0.0
            for j in range(0,n):
                if (maxSim_i<matrix[i,j]):
                    maxSim_i=matrix[i,j]

            sumSim_i=sumSim_i+maxSim_i*(m*weight[i])

        """
        for j in range(0,n):
            maxSim_j=0.0
            for i in range(0,m):
                if (maxSim_j<matrix[i,j]):
                    maxSim_j=matrix[i,j]

            sumSim_j=sumSim_j+maxSim_j

        sim=float(sumSim_i+sumSim_j)/float(m+n)
        """
        sim=float(sumSim_i)/float(m)
        return sim

if __name__ == "__main__":
    ws=WordnetSimilarity()
    print ws.getScore(ws.getSimilarityMatrix(["dog","animal"],["dog","is","animal"]),[0.1,0.9])
