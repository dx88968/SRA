__author__ = 'DX'

from non_domain import NonDomainClassfier
from plsaModeler import plsaModeler
from input_data import InputData
from os import listdir
from output import output

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
                3: [0.35, 0.75],
                5: [0, 0.25, 0.5, 0.75]
        }

    def train(self,datamode,directory):
        self.dataset_type=datamode
        self.nonDomain = NonDomainClassfier()
        if datamode=="seb":
            self.nonDomain.train_dir('seb', '../SemEval/train/seb/Core/')
            self.modeler=plsaModeler('seb', '../SemEval/train/seb/Core/')
        else:
            self.nonDomain.train_all('beetle', '../SemEval/train/beetle/Core/')
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
            for r in question["referenceAnswers"]:
                grade=""
                for sr in r["studentAnswers"]:
                    if self.nonDomain.test(sr["text"]):
                        if mode==2 or mode==3:
                            grade="incorrect"
                        if mode==5:
                            grade=="non_domain"
                        rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade})

                        """
                    handle not


                    """

                    score=self.modeler.grade(id,sr["text"])
                    grade=self.predict(score)
                    rsl.append({"id": sr["id"],"Accuracy":sr["accuracy"],"Predicted":grade})

            output(self.output_filename, head, rsl)


    def predict(self, points):
        """
            convert points to an text grade based on mode
            points = []
        """
        way2 = ["incorrect", "correct"]
        way3 = ["incorrect", "contradictory", "correct"]
        way5 = ["non_domain", "irrelevant", "contradictory",
                "partially_correct_incomplete", "correct"]
        point = max(points)
        if self.mode == 2:
            if point < self.modes[2][0]:
                return way2[0]
            else:
                return way2[1]
        elif self.mode == 3:
            for i in range(2):
                if point < self.modes[3][i]:
                    return way3[i]
            return way3[2]
        elif self.mode == 5:
            for i in range(4):
                if point < self.modes[5][i]:
                    return way5[i]
            return way5[4]
        else:
            raise Exception("Wrong mode")