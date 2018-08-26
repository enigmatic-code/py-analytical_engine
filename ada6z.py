#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 7 - ada6z.py

from analytical_engine import AnalyticalEngine, Column
from enigma import raw_input, printf

# initialise the engine
ae = AnalyticalEngine(vars=14, number=Column(digits=10, dp=40), warn=1, trace=0)

from fractions import Fraction
ae = AnalyticalEngine(vars=14, number=Fraction, warn=1, trace=0)

# assemble the program
(program, labels) = ae.assemble("""
  :init
  SET v0 <- 0
  SET v1 <- 1
  SET v2 <- 2
  SET v3 <- 1
  :start
  MUL v2 v3 -> v4 v5 v6
  SUB v4. 1 -> v4
  ADD v5. 1 -> v5
  DIV v4. v5. -> v11
  DIV v11. 2 -> v11
  SUB v13. v11. -> v13
  SUB v3 1 -> v10
  BRZ finish
  ADD v2 v7. -> v7
  DIV v6 v7 -> v11
  MUL DATA v11 -> v12
  ADD v12. v13. -> v13
  SUB v10. 1 -> v10
  BRZ finish
  :loop
  SUB v6. 1 -> v6
  ADD 1 v7. -> v7
  DIV v6 v7 -> v8
  MUL v8. v11. -> v11
  SUB v6. 1 -> v6
  ADD 1 v7. -> v7
  DIV v6 v7 -> v9
  MUL v9. v11. -> v11
  MUL DATA v11 -> v12
  ADD v12. v13. -> v13
  SUB v10. 1 -> v10
  BRN loop
  :finish
  SUB 0 v13.
  PRINT
  ADD 1 v3. -> v3
  SET v6 <- 0
  SET v7 <- 0
  SET v11 <- 0
  HALT
""")

# load the program
ae.load_program(program)

# indices B[k]
k = 1
# input data, initially empty, but each result is added after computation
data = []
# instruction to start execution at, initially 0, but subsequently 4
start = labels['init']
# run the program
while True:
  # load the data and run the program
  ae.load_data(data)
  ae.run(start)
  # get the computed result from the output transcript
  r = (ae.output[-1] if ae.output else None)

  # display the computed result
  printf("B[{k}] = {r}")

  # run the program again?
  try:
    raw_input('\n[paused] >>> ')
  except EOFError:
    printf()
    break

  # add the result to the data and run it again (from instruction 4)
  data.append(r)
  start = labels['start']
  k += 2
