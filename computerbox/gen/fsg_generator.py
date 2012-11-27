#!/usr/bin/python

"""
Tools for creating a finite state grammar for PocketSphinx's HMM. It consists of
a series of nodes connected by edges, where each edge may or may not have a word
pronounced on it. The first two nodes created must be the starting and ending
nodes of the FSG.

For convenience, you can also combine sets of nodes into "supernodes" which
encapsulate them. Supernodes are specified by their own start and end nodes,
which are where all external edges will connect.

When you are done creating all your nodes, run PrintFSG(), and the FSG will be
printed to stdout.

This is useful because it produces FSGs which are much more efficient than
sphinx_jsgf2fsg.

Note that all edges in the generated FSGs have equal weight. If you want an HMM
model in which the edges coming out of a node are unequally weighted, you'll
need to do something different.
"""

_registry = []  # A list of nodes

class Node(object):
  def __init__(self):
    self.edges = []  # List of (next_node, word) pairs
    self.number = len(_registry)
    _registry.append(self)
    #print "made node number %s" % self.number

  def _GetStart(self):
    """Overridden in supernodes"""
    return self

  def _GetEnd(self):
    """Overridden in supernodes"""
    return self

  def AddEdge(self, target, phrase=""):
    words = phrase.split()
    if len(words) == 0:
      words = [None]
    current = self._GetEnd()
    # Chain intermediate nodes for all but the last word
    for word in words[:-1]:
      next = Node()
      current.edges.append((next, word))
      current = next
    target_raw_node = target._GetStart()
    current.edges.append((target_raw_node, words[-1]))

  def Print(self):
    #print "node #%s has %s edges." % (self.number, len(self.edges))
    if len(self.edges) == 0 and self.number == 1:
      return  # we're the ending node.

    prob = 1.0 / len(self.edges)
    for e in self.edges:
      if e[1]:
        text = " %s" % e[1]
      else:
        text = ""
      print "TRANSITION %d %d %f%s" % (self.number, e[0].number, prob, text)

class Supernode(Node):
  def __init__(self, start, end):
    self._start = start._GetStart()
    self._end = end._GetEnd()

  def _GetStart(self):
    return self._start

  def _GetEnd(self):
    return self._end

def PrintFSG():
  print "FSG_BEGIN"
  print "NUM_STATES %s" % len(_registry)
  print "START_STATE 0"
  print "FINAL_STATE 1"
  for node in _registry:
    node.Print()
  print "FSG_END"
