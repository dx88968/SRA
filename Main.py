__author__ = 'DX'

from non_domain import NonDomainClassfier
from plsaModeler import plsaModeler
from input_data import InputData
from os import listdir
from output import output
from contradictory import ContradictoryClassfier
from ContradictoryBigram import ContradictoryBigram
from IrrelevantDetector import IrrelevantDetector
import sys

class SRA:
    def __init__(self):
        """
            dataset_type: "beetle" or "seb"
            path: the path of test data
            mode: 2, 3 or 5
            output_filename: "filename"
        """

        self.contradict=ContradictoryClassfier()
        self.nonDomain = NonDomainClassfier()
        self.contradictBigram=ContradictoryBigram()
        self.irr=IrrelevantDetector()

    def train(self,datamode,directory):
        self.dataset_type=datamode
        self.datamode=datamode

        if datamode=="seb":
            self.nonDomain.train_dir('seb', directory)
            self.modeler=plsaModeler('seb', directory)
            self.modes={
                2: [0.4],
                3: [0.4],
                5: [0.25,0.4]
            }
        else:
            self.nonDomain.train_dir('beetle', directory)
            self.modeler=plsaModeler("beetle", directory)
            self.modes={
                2: [0.5],
                3: [0.5],
                5: [0,0.5]
            }
        self.contradictBigram.load(datamode,directory)
        self.modeler.train()

    #mode indicates if it uses 2-way,3-way or 5-way
    def test(self,mode,inputdir,outputdir):
        head = ["id","grade" ,"Accuracy","Predicted"]
        self.mode=mode
        rsl=[]
        files = listdir(inputdir)
        reader = InputData(self.dataset_type, inputdir)
        for filename in files:
            question = reader.readFile(filename)
            id = question["id"]
            stuAns = []
            for r in question["referenceAnswers"]:   
                for sr in r["studentAnswers"]:
                    stuAns.append(sr)
            for sr in question["otherStudentAnswers"]:
                stuAns.append(sr)
                
            for sr in stuAns:
                grade=""
                if self.nonDomain.test(sr["text"]):
                    if mode==2 or mode==3:
                        grade="incorrect"
                    if mode==5:
                        grade="non_domain"
                    rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade,"grade":"NA"})
                    print rsl[len(rsl)-1]
                    continue

                if self.contradictBigram.isContradictory(id,sr["text"]) or self.contradict.isContradictory(self.modeler.getReferences(id),sr["text"]):
                    if mode==2:
                        grade="incorrect"
                    if mode==3 or mode==5:
                        grade="contradictory"
                    rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade,"grade":"NA"})
                    print rsl[len(rsl)-1]
                    continue

                score=self.modeler.grade(id,sr["text"])
                if self.datamode== "beetle":
                    self.irr.build(self.modeler.getReferences(id))
                    if self.irr.isIrrelevent(sr["text"]):
                        score=-1
                grade=self.predict(score)
                rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade,"grade":score})
                print rsl[len(rsl)-1]
            
            output(outputdir, head, rsl)


    def predict(self, point):
        """
            convert points to an text grade based on mode
            points = []
        """
        way2 = ["incorrect", "correct"]
        way3 = ["incorrect", "correct"]
        way5 = ["irrelevant","partially_correct_incomplete", "correct"]
        if self.mode == 2:
            if point < self.modes[2][0]:
                return way2[0]
            else:
                return way2[1]
        elif self.mode == 3:
            if point < self.modes[3][0]:
                return way3[0]
            else:
                return way3[1]
        elif self.mode == 5:
            for i in range(2):
                if point < self.modes[5][i]:
                    return way5[i]
            return way5[2]
        else:
            raise Exception("Wrong mode")

def main():
    argv = sys.argv
    
    if len(argv) == 1:
        print "Using default parameters"
        (dataset, n, train, test, output) = ('seb', '5', "../SemEval/train/seb/Core/","../SemEval/train/seb/Core/","output")
    elif len(argv) != 6:
        print "Wrong Parameters!"
        print "Main.py dataset n-way trainingDir testDir output"
        return
    else:
        (dataset, n, train, test, output) = argv[1:]
    if(dataset not in ["beetle", "seb"]):
        print "dataset only can be beetle or seb"
        return 
    if(n not in ('2', '3', '5')):
        print "n-way must be 2,3 or 5"
        return

    sra=SRA()
    print "start training"
    sra.train(dataset, train)
    print "training complete"
    sra.test(int(n), test, output)

if __name__ == "__main__":
    main()

