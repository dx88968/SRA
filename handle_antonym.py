from pystanford_parser import Parser
from nltk.corpus import wordnet as wn

class HandleAntonym(object):
    """
        handleAntonym, depended on the ParserServer.java (stanford_parser)
        and nltk, wordnet.
    """
    def __init__(self):
        self.parser = Parser()
        self.count_types=[u"VBG"]

    def process(self, sentence):
        (tags, typedepend) = self.parser.parser(sentence)
        not_count = 0

        for t in typedepend:
            if t[0] == u"neg":
                windex = t[1][1]
                not_index = t[2][1]
                vtype = tags[windex][1]
                if vtype in self.count_types:
                    tags[not_index][0] = 0
                    not_count += 1
                else:
                    n_word = wn.synsets(tags[windex][0])[0]
                    ants = n_word.lemmas[0].antonyms()
                    if len(ants) == 0:
                        tags[not_index][0] = 0
                        not_count += 1
                    else:
                        tags[not_index][0] = 0
                        tags[windex][0] = unicode(ants[0].name)
        import unicodedata

        return (bool(not_count % 2), 
            " ".join(
                [unicodedata.normalize('NFKD', item[0] ).encode('ascii','ignore')
                    for item in tags
                        if (item[0] != 0)] ))

    def isNeg(self,sentence):
        (tags, typedepend) = self.parser.parser(sentence)
        not_count = 0

        for t in typedepend:
            if t[0] == u"neg":
                windex = t[1][1]
                not_index = t[2][1]
                vtype = tags[windex][1]
                if vtype in self.count_types:
                    tags[not_index][0] = 0
                    not_count += 1
                else:
                    try:
                        n_word = wn.synsets(tags[windex][0])[0]
                        ants = n_word.lemmas[0].antonyms()
                        tags[not_index][0] = 0
                        not_count += 1
                        tags[not_index][0] = 0
                    except:
                        continue

        import unicodedata

        return (bool(not_count % 2),
            " ".join(
                [unicodedata.normalize('NFKD', item[0] ).encode('ascii','ignore')
                    for item in tags
                        if (item[0] != 0)] ))


def test(sentence):
    h = HandleAntonym()
    return h.process(sentence)

if __name__ == "__main__":
    print test("dog is not bad")
