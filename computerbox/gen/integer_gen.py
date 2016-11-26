#!/usr/bin/python

import fsg_generator as fsg

def nzdigit():
  start = fsg.Node()
  end = fsg.Node()
  start.AddEdge(end, "ONE")
  start.AddEdge(end, "TWO")
  start.AddEdge(end, "THREE")
  start.AddEdge(end, "FOUR")
  start.AddEdge(end, "FIVE")
  start.AddEdge(end, "SIX")
  start.AddEdge(end, "SEVEN")
  start.AddEdge(end, "EIGHT")
  start.AddEdge(end, "NINE")
  return fsg.Supernode(start, end)

def teens():
  start = fsg.Node()
  end = fsg.Node()
  start.AddEdge(end, "TEN")
  start.AddEdge(end, "ELEVEN")
  start.AddEdge(end, "TWELVE")
  start.AddEdge(end, "THIRTEEN")
  start.AddEdge(end, "FOURTEEN")
  start.AddEdge(end, "FIFTEEN")
  start.AddEdge(end, "SIXTEEN")
  start.AddEdge(end, "EIGHTEEN")
  start.AddEdge(end, "NINETEEN")
  return fsg.Supernode(start, end)

def tens():
  start = fsg.Node()
  end = fsg.Node()
  start.AddEdge(end, "TWENTY")
  start.AddEdge(end, "THIRTY")
  start.AddEdge(end, "FORTY")
  start.AddEdge(end, "FIFTY")
  start.AddEdge(end, "SIXTY")
  start.AddEdge(end, "SEVENTY")
  start.AddEdge(end, "EIGHTY")
  start.AddEdge(end, "NINETY")
  return fsg.Supernode(start, end)

def two_d():
  start = fsg.Node()
  end = fsg.Node()
  tens_node = tens()
  teens_node = teens()
  nz = nzdigit()

  start.AddEdge(teens_node)
  start.AddEdge(tens_node)
  start.AddEdge(nz)

  tens_node.AddEdge(nz)
  tens_node.AddEdge(end)

  teens_node.AddEdge(end)

  nz.AddEdge(end)

  return fsg.Supernode(start, end)

def three_d():
  start = fsg.Node()
  end = fsg.Node()
  nz = nzdigit()
  two_d_node = two_d()

  start.AddEdge(nz)
  start.AddEdge(two_d_node)
  nz.AddEdge(two_d_node, "HUNDRED")
  nz.AddEdge(end, "HUNDRED")
  two_d_node.AddEdge(end)

  return fsg.Supernode(start, end)

def six_d():
  start = fsg.Node()
  end = fsg.Node()
  extra = fsg.Node()
  three_d_node = three_d()
  other = three_d()

  start.AddEdge(three_d_node)
  start.AddEdge(other)
  three_d_node.AddEdge(extra, "THOUSAND")
  extra.AddEdge(other)
  extra.AddEdge(end)
  other.AddEdge(end)

  return fsg.Supernode(start, end)

def nine_d():
  start = fsg.Node()
  end = fsg.Node()
  extra = fsg.Node()
  three_d_node = three_d()
  other = six_d()

  start.AddEdge(three_d_node)
  start.AddEdge(other)
  three_d_node.AddEdge(extra, "MILLION")
  extra.AddEdge(other)
  extra.AddEdge(end)
  other.AddEdge(end)

  return fsg.Supernode(start, end)

def twelve_d():
  start = fsg.Node()
  end = fsg.Node()
  extra = fsg.Node()
  three_d_node = three_d()
  other = nine_d()

  start.AddEdge(three_d_node)
  start.AddEdge(other)
  three_d_node.AddEdge(extra, "BILLION")
  extra.AddEdge(other)
  extra.AddEdge(end)
  other.AddEdge(end)

  return fsg.Supernode(start, end)

def integer():
  start = fsg.Node()
  end = fsg.Node()
  number = twelve_d()
  
  start.AddEdge(end, "ZERO")
  start.AddEdge(number)
  start.AddEdge(number, "MINUS")
  start.AddEdge(number, "NEGATIVE")

  number.AddEdge(end)

  return fsg.Supernode(start, end)

def digit():
  start = fsg.Node()
  end = fsg.Node()
  nz = nzdigit()

  start.AddEdge(nz)
  nz.AddEdge(end)
  start.AddEdge(end, "ZERO")
  start.AddEdge(end, "OH")

  return fsg.Supernode(start, end)

def number():
  start = fsg.Node()
  end = fsg.Node()
  int_node = integer()
  digit_node = digit()

  start.AddEdge(int_node)
  int_node.AddEdge(digit_node, "POINT")
  int_node.AddEdge(end)

  oh_point = fsg.Node()
  start.AddEdge(oh_point, "OH")
  oh_point.AddEdge(digit_node, "POINT")

  digit_node.AddEdge(digit_node)
  digit_node.AddEdge(end)

  return fsg.Supernode(start, end)

def value(expr):
  # expr is the supernode of an entire expression that we can encapsulate in
  # parentheses here.
  start = fsg.Node()
  end = fsg.Node()
  n = number()

  start.AddEdge(n)
  n.AddEdge(end)

  start.AddEdge(expr, "OPEN_PAREN")
  expr.AddEdge(end, "CLOSE_PAREN")

  return fsg.Supernode(start, end)

def unary(expr):
  start = fsg.Node()
  end = fsg.Node()
  v = value(expr)

  start.AddEdge(v)
  start.AddEdge(v, "THE SQUAREROOT OF")

  v.AddEdge(end)
  v.AddEdge(end, "SQUARED")
  v.AddEdge(end, "CUBED")
  v.AddEdge(end, "FACTORIAL")

  return fsg.Supernode(start, end)

def binary(expr):
  start = fsg.Node()
  end = fsg.Node()
  u = unary(expr)

  start.AddEdge(u)
  u.AddEdge(end)
  u.AddEdge(u, "PLUS")
  u.AddEdge(u, "MINUS")
  u.AddEdge(u, "TIMES")
  u.AddEdge(u, "DIVIDED BY")
  u.AddEdge(u, "TO THE POWER OF")

  return fsg.Supernode(start, end)

def expr():
  """ Clever trick alert: the contents of an expression can themselves contain
  expressions within parentheses, so we pass our start and end nodes to our
  internals before they are built."""
  start = fsg.Node()
  end = fsg.Node()
  super = fsg.Supernode(start, end)
  b = binary(super)
  start.AddEdge(b)
  b.AddEdge(end)

  return super

# These are the true starting and ending nodes. The end node must be separate
# from expr's end node because expr's end can loop back into a CLOSE_PAREN,
# while the final end node cannot (due to the HMM deciding we're done).
start = fsg.Node()
end = fsg.Node()
e = expr()

start.AddEdge(e)
e.AddEdge(end)

#integer()

fsg.PrintFSG()
