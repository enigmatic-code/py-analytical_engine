#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/14/running-the-first-program-part-2/
# Program 3 - factoria1.py

from analytical_engine import AnalyticalEngine

# initialise the engine
ae = AnalyticalEngine(vars=3, number=int)

# load the program to compute factorial(12)
n = 12
ae.load_program([
  # initialisation
  ['SET', 0, n],
  ['SET', 1, 1],
  ['SET', 2, 1],
  # operation 1: v[2] = v[0] * v[2]
  ['MUL'],
  ['LOAD', 0],
  ['LOAD', 2],
  ['STORE', 2],
  # operation 2: v[0] = v[0] - 1
  ['SUB'],
  ['LOAD', 0],
  ['LOAD', 1],
  ['STORE', 0],
  # branch if non-zero to operation 1
  ['BRN', -9],
  # end
  ['HALT'],
])

# run the program
ae.run()

# the result is in v[2]
print("factorial({n}) = {f}".format(n=n, f=ae.v[2]))
