#!/usr/bin/python

### Use InputData(directory_path(defalut: ''), dataset(defalut: 'beetle')) to make an instance,
##  Then call InputData.readFile(file_name, dataset(defalut is 'beetle')) to read file.
##  file_name should not include path if directory_path is already set.
##
##  The output is a dictionary, according to dataset
##  For 'beetle':
##      the dictionary is
##          { 'id' -> question id,
##            'text' -> question text,
##            'referenceAnswers' -> [ 0 : { 'id' -> reference answer id
##                                          'category' -> reference answer category(Best/Minimal)
##                                          'text' -> reference answer text
##                                          'studentAnswers' -> [ 0 : { 'id' -> student answer id
##                                                                      'accuracy' -> the accuracy for this reference answer
##                                                                      'text' -> student answer text
##                                                                    }
##                                                                1 : ...
##                                                              ]
##                                        }
##                                    1 : ...
##                                  ]
##            'otherStudentAnswers' -> [ 0 : { 'id' -> student answer id
##                                             'accuracy' -> the accuracy for this reference answer
##                                             'text' -> student answer text
##                                           }
##                                       1 : ...
##                                     ]
##          }
##
##  For 'seb'
##      the dictionary is
##          { 'id' -> question id,
##            'text' -> question text,
##            'referenceAnswer' -> [ 0 : { 'id' -> reference answer id
##                                         'text' -> reference answer text
##                                         'studentAnswers' -> [ 0 : { 'id' -> student answer id
##                                                                      'accuracy' -> the accuracy for this reference answer
##                                                                      'text' -> student answer text
##                                                                    }
##                                                                1 : ...
##                                                              ]
##                                        }
##                                  ]
##            'otherStudentAnswers' -> [ 0 : { 'id' -> student answer id
##                                             'accuracy' -> the accuracy for this reference answer
##                                             'text' -> student answer text
##                                           }
##                                       1 : ...
##                                     ]
##          }

## In addition, the directory can be read with readDir

import os
from xml.etree import ElementTree
from os import walk



class InputData(object):

    def __init__(self, dataset, path = ''):
        self.path = path
        self.dataset = dataset.lower()
        if (self.dataset != 'beetle') and (self.dataset != 'seb'):
            raise Exception("Wrong dataset")
        self.questions = []

    def readDir(self, dict_path = ''):
        if self.path == '':
            self.path = dict_path
        if not os.path.isdir(self.path):
            print 'Path not exist!'
        else:  
            file_name_list = []
            for (dirpath, dirnames, filenames) in walk(self.path):
                file_name_list.extend(filenames)
                break

            for file_name in file_name_list:
                self.questions.append(self.readFile(file_name))
            return self.questions
                

    def readFile(self, file_name):
        # self.dataset = dataset.lower()
        self.file = file_name
        
        # reset question, let the instance resueable.
        self.question = {}

        if not os.path.isfile( os.path.join(self.path, self.file)):
            print 'File not exist!'
        else:
            self.document = ElementTree.parse( os.path.join(self.path, self.file))
            self.root = self.document.getroot()
            self.question['id'] = self.root.attrib['id']
            self.question['text'] = self.root[0].text
            
            if self.dataset == 'beetle':
                return self._readBeetle()
            else:
                return self._readSeb()

            
            
    def _readBeetle(self):
        self.question['referenceAnswers'] = []
        for ans in self.root[1]:
            each_ref_ans = {}
            for key, value in ans.attrib.items():
                if key != 'fileID':
                    each_ref_ans[key] = value
            each_ref_ans['text'] = ans.text
            each_ref_ans['studentAnswers'] = []
            self.question['referenceAnswers'].append(each_ref_ans)
        self.question['otherStudentAnswers'] = []

        for ans in self.root[2]:
            each_stu_ans = {}
            ans_id = None
            for key, value in ans.attrib.items():
                if key == 'answerMatch':
                    ans_id = value
                elif key != 'count':
                    each_stu_ans[key] = value
            each_stu_ans['text'] = ans.text
            if (ans_id == None) or (each_stu_ans['accuracy'] != correct):                        
                self.question['otherStudentAnswers'].append(each_stu_ans)
            else:
                for index in range(len(self.question['referenceAnswers'])):
                    if self.question['referenceAnswers'][index]['id'] == ans_id:
                        self.question['referenceAnswers'][index]['studentAnswers'].append(each_stu_ans)
                        break;
        
            
        #print len(self.question['referenceAnswers'])
        return self.question

    def _readSeb(self):
        self.question['referenceAnswers'] = []
        referenceAnswer = {}
        referenceAnswer['id'] = self.root[1][0].attrib['id']
        referenceAnswer['text'] = self.root[1][0].text
        referenceAnswer['studentAnswers'] = []
        self.question['otherStudentAnswers'] = []
        for ans in self.root[2]:
            each_stu_ans = {}
            for key, value in ans.attrib.items():
                each_stu_ans[key] = value
            each_stu_ans['text'] = ans.text
            if each_stu_ans['accuracy'] == 'correct':
                referenceAnswer['studentAnswers'].append(each_stu_ans)
            else:
                self.question['otherStudentAnswers'].append(each_stu_ans)
        self.question['referenceAnswers'].append(referenceAnswer)

        #print len(self.question['studentAnswers'])
        return self.question
        
# Testing code
if __name__ == '__main__':
    model = InputData('seb','../SemEval/train/seb/Core')
    result = model.readDir()
    print len(result)
    
