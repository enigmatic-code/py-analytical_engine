#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# calcuate an approximation to pi
#
# pi/2 = 1 + 1/3 + (1/3)(2/5) + (1/3)(2/5)(3/7) + ...
#
# we use 6 variables in the AE:
#
#  v0 = x (approximation to pi)
#  v1 = t (incremental term)
#  v2 = a (numerator)
#  v3 = b (denominator)
#  v4 = 1 (constant, numerator increment)
#  v5 = 2 (constant, denominator increment)

from analytical_engine import AnalyticalEngine

# initialise the engine
ae = AnalyticalEngine(vars=6, warn=1, trace=0)

(program, _) = ae.assemble("""
  :init
  SET v1 <- 2
  SET v2 <- 1
  SET v3 <- 3
  SET v4 <- 1
  SET v5 <- 2
  :repeat
  # add in the current term
  ADD v0. v1 -> v0
  # calculate the next term: t = t * a / b
  MUL v1. v2 -> v1
  DIV v1. v3 -> v1
  # have we run out of accuracy?
  BRZ exit
  # increment a and b
  ADD v2. v4 -> v2
  ADD v3. v5 -> v3
  BRA repeat
  :exit
  HALT
""")

# load the program
ae.load_program(program)

# run the program
ae.run()

# the result is in v0
print("pi = {r}".format(r=ae.v[0]))
