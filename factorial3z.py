#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 6 - alternative implementation of factorial3.py using destructive reads

from analytical_engine import AnalyticalEngine, Column

import sys
n = (40 if len(sys.argv) < 2 else int(sys.argv[1]))

# initialise the engine
ae = AnalyticalEngine(vars=3, number=Column(digits=50), warn=1, trace=0)

(program, _) = ae.assemble("""
  :init
  SET v0 <- {n}
  SET v1 <- 1
  SET v2 <- 1
  :loop
  # operation 1: v2 = v0 * v2
  MUL v0 v2. -> v2
  # operation 2: v0 = v0 - 1
  SUB v0. 1 -> v0
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
print("factorial({n}) = {f}".format(n=n, f=ae.v[2]))
