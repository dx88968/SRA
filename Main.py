__author__ = 'DX'

from non_domain import NonDomainClassfier
from plsaModeler import plsaModeler
from input_data import InputData
from os import listdir
from output import output
from contradictory import ContradictoryClassfier

class SRA:
    def __init__(self):
        """
            dataset_type: "beetle" or "seb"
            path: the path of test data
            mode: 2, 3 or 5
            output_filename: "filename"
        """
        self.modes={
                2: [0.75],
                3: [0.75],
                5: [0.4, 0.75]
        }
        self.contradict=ContradictoryClassfier()
        self.nonDomain = NonDomainClassfier()

    def train(self,datamode,directory):
        self.dataset_type=datamode

        if datamode=="seb":
            self.nonDomain.train_dir('seb', '../SemEval/train/seb/Core/')
            self.modeler=plsaModeler('seb', '../SemEval/train/seb/Core/')
        else:
            self.nonDomain.train_dir('beetle', '../SemEval/train/beetle/Core/')
            self.modeler=plsaModeler("beetle", "../SemEval/train/beetle/Core/")

        self.modeler.train()

    #mode indicates if it uses 2-way,3-way or 5-way
    def test(self,mode,inputdir,outputdir):
        head = ["id","Accuracy", "Predicted"]
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
                    rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade})
                    print rsl[len(rsl)-1]
                    continue

                """
                if self.contradict.isContradictory(self.modeler.getReferences(id),sr["text"]):
                    if mode==2:
                        grade="incorrect"
                    if mode==3 or mode==5:
                        grade="contradictory"
                    rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade})
                    print rsl[len(rsl)-1]
                    continue

                """

                score=self.modeler.grade(id,sr["text"])
                grade=self.predict(score)
                rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade})
                print rsl[len(rsl)-1]
            
            output(outputdir, head, rsl)


    def predict(self, point):
        """
            convert points to an text grade based on mode
            points = []
        """
        way2 = ["incorrect", "correct"]
        way3 = ["incorrect", "correct"]
        way5 = ["irrelevant",
                "partially_correct_incomplete", "correct"]
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

if __name__ == "__main__":
    sra=SRA()
    print "start training"
    sra.train("beetle", "../SemEval/train/beetle/Core/")
    print "training complete"
    sra.test(5,"../SemEval/train/beetle/Core/","output")

