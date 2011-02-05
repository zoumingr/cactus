#!/usr/bin/env python

"""randGraph.py outputs a random graph generated by the G(N,p) Gilbert model.
See usage for more info. 

The file format of the output is:

Line 0 contains the number of vertices V and the number of edges E.
Lines 1 to E contain the edges referenced by vertex index i, j with weight w.
  Vertices i and j, as well as weight w are integers and the indices start 
  with 0.
"""

import getopt
import random
import sys

def usage():
    print "randGraph.py -N vertex_count -p prob_of_edge -w weight"
    print "\t-N vertex_count is the number of vertices in graph"
    print "\t  Note: N must be even and an integer"
    print "\t-p prob_of_edge is the probability of an edge"
    print "\t-w weight is the weight of the edge, uniform(-w, w)"
    print ""
    print "\t  Default values are: N=1000, p=1.0, w=5"
    print "\tGenerates a random graph according to the G(N,p) Gilbert model"
    print "\tSee http://en.wikipedia.org/wiki/Random_graph for more details"

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'N:p:w:h')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(-1)

    # default values
    N = 1000
    p = 1.0
    w = 5
    for o, a in optlist:
       if o == '-N':
           N = int(a)
       elif o == '-p':
           p = float(a)
       elif o == '-w':
           w = int(a)
       elif o == '-h':
           usage()
           sys.exit()
       else:
           assert False, "unhandled option"

    if N % 2 != 0:
        print "N cannot be an odd number"
        print ""
        usage()
        sys.exit()

    edges = []
    for i in xrange(N):
        for j in xrange(i+1,N):
            if p == 1.0 or random.uniform(0, 1.0) <= p:
                weight = random.randint(-w, w)
                string = "%d %d %d" % (i, j, weight)
                edges.append(string)

    print N, len(edges)
    for e in edges:
        print e

if __name__ == "__main__":
    main()