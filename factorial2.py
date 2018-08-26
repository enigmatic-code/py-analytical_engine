#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/14/running-the-first-program-part-2/
# Program 5 - factorial2.py

from analytical_engine import AnalyticalEngine, Column

# compute factorial(n)
from sys import argv
n = (40 if len(argv) < 2 else int(argv[1]))

# initialise the engine
ae = AnalyticalEngine(vars=3, number=Column(digits=50))

# load the program
ae.load_program([
  # initialisation
  ['SET', 0, n],
  ['SET', 1, 1],
  ['SET', 2, 1],
  # operation 1: v2 = v0 * v2
  ['MUL'],
  ['LOAD', 0],
  ['LOAD', 2],
  ['STORE', 2],
  # operation 2: v0 = v0 - 1
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

# the result is in v2
print("factorial({n}) = {r}".format(n=n, r=ae.v[2]))
