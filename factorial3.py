#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 6 - factorial3.py

from analytical_engine import AnalyticalEngine, Column

# compute factorial(n)
from sys import argv
n = (40 if len(argv) < 2 else int(argv[1]))

# initialise the engine
ae = AnalyticalEngine(vars=3, number=Column(digits=50), trace=1)

(program, _) = ae.assemble("""
  :init
  SET 0 <- {n}
  SET 1 <- 1
  SET 2 <- 1
  :loop
  # operation 1: v2 = v0 * v2
  MUL 0 2 -> 2
  # operation 2: v0 = v0 - 1
  SUB 0 1 -> 0
  # branch if non-zero to operation 1
  BRN loop
  # end
  HALT
""".format(n=n))

# load the program to compute factorial(n)
ae.load_program(program)

# run the program
ae.run()

# the result is in v2
print("factorial({n}) = {r}".format(n=n, r=ae.v[2]))
