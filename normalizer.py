#!/usr/bin/env python

import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

import time

class Tokenizer(object):
    def tokenize(self, text):
        text = text.translate(None, string.punctuation)
        tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
        filtered_words = [w for w in tokens if not w.lower() in stopwords.words('english')]
        return filtered_words

class Stemmer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
        
    def stem(self, word):
        return self.stemmer.stem(word)

    def stem_words(self, words):
        result = []
        for word in words:
            result.append(self.stem(word))
        return result

class Lemmatizer(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        
    def lemmatize(self, word):
        return self.lemmatizer.lemmatize(word)

    def lemmatize_words(self, words):
        result = []
        for word in words:
            result.append(self.lemmatize(word))
        return result
    
if __name__ == '__main__':
    start_time = time.time()
    Lemmatizer = Lemmatizer()
    tokenizer = Tokenizer()
    s = 'I have a command line program in Python, that takes quite a while to finish. I want to know the exact time it takes to finish running.'
    #print Lemmatizer.stem_words(tokenizer.tokenize(s))
    print Lemmatizer.lemmatize('chosen')
    stemmer = Stemmer()
    print stemmer.stem('having')
    print time.time() - start_time, "seconds"
    
