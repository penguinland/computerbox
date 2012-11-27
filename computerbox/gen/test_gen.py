#!/usr/bin/python

import fsg_generator

start = fsg_generator.Node()
end = fsg_generator.Node()
middle = fsg_generator.Node()
start.AddEdge(middle, "ONE")
start.AddEdge(middle, "TWO")
start.AddEdge(middle, "THREE")
middle.AddEdge(end, "STOP")
middle.AddEdge(end, "END")

fsg_generator.PrintFSG()
