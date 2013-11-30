from py4j.java_gateway import JavaGateway

class Parser(object):
    """
        a port to stanford parser,
        return Tagging and Typed dependencies
    """
    def __init__(self):
        self.gateway = JavaGateway()
    
    def parser(self, sentence):
        rsl = self.gateway.parser(sentence).split("@")
        tagstr = rsl[0][1:-1]
        typed_dependencies = rsl[1][1:-2]
        
        tags = []
        for pair in tagstr.split(", "):
            (k,v) = pair.strip().split("/")
            tags.append( [k, v] )

        typedd = []
        for pair in typed_dependencies.split("), "):
            (d,c) = pair.strip().split("(")
            (c1,c2) = c.split(",")
            (c1w, c1i) = c1.split("-")
            (c2w, c2i) = c2.split("-")
            typedd.append(
                    (d, (c1w, int(c1i) - 1),
                        (c2w, int(c2i) - 1)))
        return (tags, typedd)

        
        
        
