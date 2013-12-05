#!/usr/bin/env python

import re, enchant

class SpellReplacer(object):
    def __init__(self, dict_name = 'en_GB'):
        self.spell_dict = enchant.Dict(dict_name)
        self.alphabet = "abcdefghijklmnopqrstuvwxyz'"
        text = file('high_frequency_words.txt').read()
        self.hfwords = re.findall('[a-z\']+', text.lower())
    
    def replace(self, word):
        if self.spell_dict.check(word.lower()):
            return word.lower()
        elif self.spell_dict.check(word):
            return word
        else:
            return self.edits1(word.lower())

    def edits1(self, word):
        if self.spell_dict.check(word.capitalize()):
            return word.capitalize()
        
        change = []
        
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        inserts    = [a + c + b for a, b in splits for c in self.alphabet]
        deletes    = [a + b[1:] for a, b in splits if b]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]

        changeWords = inserts + deletes + replaces + transposes 
        for word in changeWords:
            if self.spell_dict.check(word) and word in self.hfwords:
                return word
        
        for word in changeWords:
            if self.spell_dict.check(word):
                return word

        return None

if __name__ == "__main__":
    replacer = SpellReplacer()
    print replacer.replace('John')
