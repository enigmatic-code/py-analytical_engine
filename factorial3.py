#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 6 - factorial3.py

from analytical_engine import AnalyticalEngine, Column, assemble

import sys
n = (40 if len(sys.argv) < 2 else int(sys.argv[1]))

(program, _) = assemble("""
  :init
  SET 0 <- {n}
  SET 1 <- 1
  SET 2 <- 1
  :loop
  # operation 1: v[2] *= v[0]
  MUL 0 2 -> 2
  # operation 2: v[2] -= 1
  SUB 0 1 -> 0
  # branch if non-zero to operation 1
  BRN loop
  # end
  HALT
""".format(n=n))

# initialise the engine
p = AnalyticalEngine(vars=3, number=Column(digits=50), trace=1)

# load the program to compute factorial(n)
p.load_program(program)

# run the program
p.run()

# the result is in v[2]
print("factorial({n}) = {f}".format(n=n, f=p.v[2]))
