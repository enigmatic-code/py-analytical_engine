#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
# Program 7 - ada6.py

from analytical_engine import AnalyticalEngine, Column, assemble
from enigma import raw_input, printf

# assemble the program
(program, labels) = assemble("""
  :init
  SET 0 <- 0
  SET 1 <- 1
  SET 2 <- 2
  SET 3 <- 1
  :start
  MUL 2 3 -> 4 5 6
  SUB 4 1 -> 4
  ADD 5 1 -> 5
  DIV 4 5 -> 11
  DIV 11 2 -> 11
  SUB 13 11 -> 13
  SUB 3 1 -> 10
  BRZ finish
  ADD 2 7 -> 7
  DIV 6 7 -> 11
  MUL DATA 11 -> 12
  ADD 12 13 -> 13
  SUB 10 1 -> 10
  BRZ finish
  :loop
  SUB 6 1 -> 6
  ADD 1 7 -> 7
  DIV 6 7 -> 8
  MUL 8 11 -> 11
  SUB 6 1 -> 6
  ADD 1 7 -> 7
  DIV 6 7 -> 9
  MUL 9 11 -> 11
  MUL DATA 11 -> 12
  ADD 12 13 -> 13
  SUB 10 1 -> 10
  BRN loop
  :finish
  SUB 0 13
  PRINT
  ADD 1 3 -> 3
  SET 7 <- 0
  SET 13 <- 0
  HALT
""")

# initialise the engine
p = AnalyticalEngine(vars=14, number=Column(digits=10, dp=40), trace=0)

# load the program
p.load_program(program)

# indices B[k]
k = 1
# input data, initially empty, but each result is added after computation
data = []
# instruction to start execution at, initially 0, but subsequently 4
start = labels['init']
# run the program
while True:
  # load the data and run the program
  p.load_data(data)
  p.run(start)
  # get the computed result from the output transcript
  r = (p.output[-1] if p.output else None)

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
