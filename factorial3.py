#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 6 - factorial3.py

from analytical_engine import AnalyticalEngine, Column

import sys
n = (40 if len(sys.argv) < 2 else int(sys.argv[1]))

# initialise the engine
ae = AnalyticalEngine(vars=3, number=Column(digits=50), trace=1)

(program, _) = ae.assemble("""
  :init
  SET 0 <- {n}
  SET 1 <- 1
  SET 2 <- 1
  :loop
  # operation 1: v[2] = v[0] * v[2]
  MUL 0 2 -> 2
  # operation 2: v[0] = v[0] - 1
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

# the result is in v[2]
print("factorial({n}) = {f}".format(n=n, f=ae.v[2]))
