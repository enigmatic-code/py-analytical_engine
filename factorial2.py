#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/14/running-the-first-program-part-2/
# Program 5 - factorial2.py

from analytical_engine import AnalyticalEngine, Column

# initialise the engine
p = AnalyticalEngine(vars=3, number=Column(digits=50))

# load the program to compute factorial(40)
n = 40
p.load_program([
  # initialisation
  ['SET', 0, n],
  ['SET', 1, 1],
  ['SET', 2, 1],
  # operation 1: v[2] *= v[0]
  ['MUL'],
  ['LOAD', 0],
  ['LOAD', 2],
  ['STORE', 2],
  # operation 2: v[2] -= 1
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
p.run()

# the result is in v[2]
print("factorial({n}) = {f}".format(n=n, f=p.v[2]))
