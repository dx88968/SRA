#!/usr/bin/env python2.7

def output(file_name, head, out):
    """
        head: [ ]
        out: [{"id": ,"fold":"", "actual":, "predicted":"", ...  }, 
            {}]
    """
    f = open(file_name, "w")
    f.write("%s\n" % "\t".join(head))
    for item in out:
        o = [str(item[k]) for k in head]
        f.write("%s\n" % "\t".join(o))
    f.close()
