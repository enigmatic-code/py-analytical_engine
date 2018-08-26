#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# calcuate square roots (using Newton's method)
# (using non-destructive reads and overwriting writes)

from analytical_engine import AnalyticalEngine, Column

from sys import argv
n = (2 if len(argv) < 2 else argv[1])

# we use 6 variables in the AE:
# v0 = 0 (constant)
# v1 = 0.5 (constant, we multiply by 0.5 instead of dividing by 2)
# v2 = n (input parameter)
# v3 = x (output parameter, approximation to square root)
# v4 = x' (previous value of x)
# v5 = t (temporary variable)

# initialise the engine using 10.40f numbers
ae = AnalyticalEngine(vars=6, number=Column(digits=10, dp=40), warn=0, trace=0)

(program, _) = ae.assemble("""
  :init
  SET v0 <- 0
  SET v1 <- 0.5
  SET v2 <- {n}
  # initial guess: x = n * 0.5
  MUL v1 v2 -> v3
  :loop
  # save current guess
  ADD v3 0 -> v4
  # x = (n / x + x) * 0.5
  DIV v2 v3 -> v5
  ADD v5 v3 -> v5
  MUL v5 v1 -> v3
  # test against previous value
  SUB v3 v4
  BRN loop
  HALT
""".format(n=n))

# load the program
ae.load_program(program)

# run the program
ae.run()

# the result is in v3
print("sqrt({n}) = {r}".format(n=n, r=ae.v[3]))
