from nltk.corpus import wordnet as wn

def isantonym(word1, word2):
    """
        judge whether two word are antonym
    """

    w1_lemma = [lemma for lemma in wn.lemmas(word1)]
    w1_antonyms = set()
    for lemma in w1_lemma:
        for antonym in lemma.antonyms():
            w1_antonyms.add(antonym.name)

    if word2 in w1_antonyms:
        return True
    else:
        return False

def antonyms(word):
    """
        return all antonyms of word
    """

    lemmas = [lemma for lemma in wn.lemmas(word)]
    antonyms = set()
    for lemma in lemmas:
        for antonym in lemma.antonyms():
            antonyms.add(antonym.name)
    return antonyms
