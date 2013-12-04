from py4j.java_gateway import JavaGateway

class Parser(object):
    """
        a port to stanford parser,
        return Tagging and Typed dependencies
    """
    def __init__(self):
        self.gateway = JavaGateway()
    
    def parser(self, sentence):
        rsl = self.gateway.parser(sentence).split("@@@@@@")
        tagstr = rsl[0]
        typed_dependencies = rsl[1]
        
        tags = []
        for pair in tagstr.split("|||"):
            if pair == '':
                continue
            (k,v) = pair.strip().split("///")
            tags.append( [k, v] )

        typedd = []
        for pair in typed_dependencies.split("|||"):
            if pair == '':
                continue
            (r,g,v) = pair.strip().split("///")
            
            gg = g.split("-")
            if len(gg) >= 3:
                gw = "-".join(gg[0:-1])
            else:
                gw = gg[0]
            gi = gg[-1]

            vv = v.split("-")
            if len(vv) >= 3:
                vw = "-".join(vv[0:-1])
            else:
                vw = vv[0]
            vi = vv[-1]

            try:
                typedd.append(
                        (r, (gw, int(gi) - 1),
                            (vw, int(vi) - 1)))
            except:
                typedd.append((r, (gw,1), (vw, 1)))
        return (tags, typedd)

        
        
        
