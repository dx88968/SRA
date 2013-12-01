from nltk.corpus import wordnet as wn

def antonym(word1, word2):
    """
        judge whether two word are antonym
    """

    w1_lemma = [lemma for lemma in wn.lemmas(word1)]
    w1_antonyms = []
    for lemma in w1_lemma:
        for antonym in lemma.antonyms():
            w1_antonyms.append(antonym.name)

    if word2 in w1_antonyms:
        return True
    else:
        return False
