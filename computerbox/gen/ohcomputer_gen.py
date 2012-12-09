#!/usr/bin/python

import fsg_generator

start = fsg_generator.Node()
end = fsg_generator.Node()

# To be honest, we want unknown noises to be more likely than the important
# phrase. Consequently, I have edited the probabilities in the .fsg file from
# what this generates.
start.AddEdge(end, "OH COMPUTER BOX")
start.AddEdge(end, "UNK")

fsg_generator.PrintFSG()
