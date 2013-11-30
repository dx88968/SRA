#!/usr/bin/env python

import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from spell_correct import SpellReplacer

import time

class Tokenizer(object):
    def __init__(self):
        self.replacer = SpellReplacer()
        
    def tokenize(self, text):
        text = text.translate(None, string.punctuation).lower()
        tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
        filtered_words = [w for w in tokens if not w in stopwords.words('english')]
        corrected_words = []
        for w in filtered_words:
            neww = self.replacer.replace(w)
            if neww != None:
                corrected_words.append(neww)
        return corrected_words

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
    s = 'I have a comsmand line program in Python, that takes quite a while to finish. I want to know the exact time it takes to finish running.'
    print tokenizer.tokenize(s)
    print time.time() - start_time, "seconds"
    
