#!/usr/bin/python

import fsg_generator as fsg

start = fsg.Node()
end = fsg.Node()

read = fsg.Node()
start.AddEdge(read, "READ ME")
read.AddEdge(end, "THAT ONE")
read.AddEdge(end, "PREVIOUS ONE")
read.AddEdge(end, "THE PREVIOUS ONE")
start.AddEdge(end, "STOP READING HEADLINES")
start.AddEdge(end, "STOP READING NEWS")

fsg.PrintFSG()
