#!/usr/bin/python

import fsg_generator as fsg

"""
Future Commands:
Read me all headlines
read me science headlines
read me world headlines
read me US headlines
weather report
weather forecast
calculate
"""

start = fsg.Node()
end = fsg.Node()

headlines_start = fsg.Node()
headlines_end = fsg.Node()
start.AddEdge(headlines_start, "READ ME")
headlines_start.AddEdge(headlines_end, "ALL")
headlines_start.AddEdge(headlines_end, "SCIENCE")
headlines_start.AddEdge(headlines_end, "YOU ESS")
headlines_start.AddEdge(headlines_end, "WORLD")
headlines_end.AddEdge(end, "HEADLINES")
headlines_end.AddEdge(end, "NEWS")

start.AddEdge(end, "WEATHER REPORT")
start.AddEdge(end, "WEATHER FORECAST")

start.AddEdge(end, "NEVER MIND")

start.AddEdge(end, "GO TO SLEEP")

# TODO: add in "calculate"

fsg.PrintFSG()
