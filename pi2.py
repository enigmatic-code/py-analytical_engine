#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# calcuate an approximation to pi
#
# pi = sum((4/(8k + 1) - 2/(8k + 4) - 1/(8k + 5) - 1/(8k + 6))(1/16)^k)
# k = 0 .. infinity
#
# [Plouffe, 1995]
#
# we use 12 variables in the AE:
#
#  v1 = 1
#  v2 = 2
#  v4 = 4
#  v5 = 5
#  v6 = 6
#  v8 = 8
#  v16 = 1/16 (* 1/16 is faster than / 16)
#
#  v0 = x (approximation to pi)
#  v3 = 8k
#  v7 = (1/16)^k
#  v9 = t (incremental term)
#  v10 = (temporary variable)

from analytical_engine import AnalyticalEngine

# initialise the engine
ae = AnalyticalEngine(vars=17, warn=1, trace=0)

(program, _) = ae.assemble("""
  :init
  # constants
  SET v1 <- 1
  SET v2 <- 2
  SET v4 <- 4
  SET v5 <- 5
  SET v6 <- 6
  SET v8 <- 8
  SET v16 <- 1/16
  SET v3 <- 0
  SET v7 <- 1
  :repeat
  # 4/(8k + 1)
  ADD v3 1 -> v10
  DIV 4 v10. -> v9
  # - 2/(8k + 4)
  ADD v3 4 -> v10
  DIV 2 v10. -> v10
  SUB v9. v10. -> v9
  # - 1/(8k + 5)
  ADD v3 5 -> v10
  DIV 1 v10. -> v10
  SUB v9. v10. -> v9
  # - 1/(8k + 6)
  ADD v3 6 -> v10
  DIV 1 v10. -> v10
  SUB v9. v10. -> v9
  # * (1/16)^k
  MUL v9. v7 -> v9
  BRZ exit
  # add in the term
  ADD v0. v9. -> v0
  # increase k
  ADD v3. 8 -> v3
  MUL v7. 16 -> v7
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
