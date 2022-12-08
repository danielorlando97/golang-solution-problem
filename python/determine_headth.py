
from math import inf
from bisect import bisect_left as bLeft, bisect_right as bRight
from collections import defaultdict

gMap = defaultdict(lambda: [[], [0]])
subs = set()


def getHealth(seq, first, last, largest):
    h, ls = 0, len(seq)
    for f in range(ls):
        for j in range(1, largest+1):
            if f+j > ls:
                break
            sub = seq[f:f+j]
            if sub not in subs:
                break
            if sub not in gMap:
                continue
            ids, hs = gMap[sub]
            a = bRight(ids, last)
            b = bLeft(ids, first)
            h += hs[a]-hs[b]
    return h


def main(genes, healths, strands):

    for id, gene in enumerate(genes):
        gMap[gene][0].append(id)
        for j in range(1, min(len(gene), 500)+1):
            subs.add(gene[:j])
    for v in gMap.values():
        for i, ix in enumerate(v[0]):
            v[1].append(v[1][i]+healths[ix])

    largest = max(map(len, genes))
    hMin, hMax = inf, 0
    for first, last, strand in strands:
        h = getHealth(strand, first, last, largest)
        hMin, hMax = min(hMin, h), max(hMax, h)
    print(hMin, hMax)


genes = ['a', 'b', 'c', 'aa', 'd', 'b', ]
healths = [1, 2, 3, 4, 5, 6]
strands = [
    [1, 5, 'caaab'],
    [0, 4, 'xyz'],
    [2, 4, 'bcdybc']
]

main(genes, healths, strands)
