def flatten(l):
    """
    Flatten 2-D list into 1-D list of each sublist's elements
    """
    return [item for sublist in l for item in sublist]

def deduplicate(l):
    """
    Deduplicate list l
    """
    return list(set(l))

def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def split_seq(seq, size):
    """
    Split a sequence into size parts of approximately equal length
    """
    newseq = []
    splitsize = 1.0/size*len(seq)
    for i in range(size):
        newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
    return newseq
