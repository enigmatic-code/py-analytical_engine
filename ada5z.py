#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# alternative implementation of ada5.py using the LOADZ opcode where appropriate

from analytical_engine import AnalyticalEngine, Column
from fractions import Fraction
from enigma import raw_input, printf

# initialise the engine
#ae = AnalyticalEngine(vars=14, number=Column(digits=10, dp=40), trace=0, warn=1)
ae = AnalyticalEngine(vars=14, number=Fraction, trace=0, warn=1)

# load the program
ae.load_program([
  # initialisation
  ['SET', 0, 0],
  ['SET', 1, 1],
  ['SET', 2, 2],
  ['SET', 3, 1],
  # operation 1
  ['MUL'],
  ['LOAD', 2],
  ['LOAD', 3],
  ['STORE', 4],
  ['STORE', 5],
  ['STORE', 6],
  # operation 2
  ['SUB'],
  ['LOADZ', 4],
  ['LOAD', 1],
  ['STORE', 4],
  # operation 3
  ['ADD'],
  ['LOADZ', 5],
  ['LOAD', 1],
  ['STORE', 5],
  # operation 4
  ['DIV'],
  ['LOADZ', 4],
  ['LOADZ', 5],
  ['STORE', 11],
  # operation 5
  ['DIV'],
  ['LOADZ', 11],
  ['LOAD', 2],
  ['STORE', 11],
  # operation 6
  ['SUB'],
  ['LOADZ', 13],
  ['LOADZ', 11],
  ['STORE', 13],
  # operation 7
  ['SUB'],
  ['LOAD', 3],
  ['LOAD', 1],
  ['STORE', 10],
  # branch if zero to operation 24
  ['BRZ', +66],
  # operation 8
  ['ADD'],
  ['LOAD', 2],
  ['LOADZ', 7],
  ['STORE', 7],
  # operation 9
  ['DIV'],
  ['LOAD', 6],
  ['LOAD', 7],
  ['STORE', 11],
  # operation 10
  ['MUL'],
  ['LOAD_DATA'],
  ['LOAD', 11],
  ['STORE', 12],
  # operation 11
  ['ADD'],
  ['LOADZ', 12],
  ['LOADZ', 13],
  ['STORE', 13],
  # operation 12
  ['SUB'],
  ['LOADZ', 10],
  ['LOAD', 1],
  ['STORE', 10],
  # branch if zero to operation 24
  ['BRZ', +45],
  # operation 13
  ['SUB'],
  ['LOADZ', 6],
  ['LOAD', 1],
  ['STORE', 6],
  # operation 14
  ['ADD'],
  ['LOAD', 1],
  ['LOADZ', 7],
  ['STORE', 7],
  # operation 15
  ['DIV'],
  ['LOAD', 6],
  ['LOAD', 7],
  ['STORE', 8],
  # operation 16
  ['MUL'],
  ['LOADZ', 8],
  ['LOADZ', 11],
  ['STORE', 11],
  # operation 17
  ['SUB'],
  ['LOADZ', 6],
  ['LOAD', 1],
  ['STORE', 6],
  # operation 18
  ['ADD'],
  ['LOAD', 1],
  ['LOADZ', 7],
  ['STORE', 7],
  # operation 19
  ['DIV'],
  ['LOAD', 6],
  ['LOAD', 7],
  ['STORE', 9],
  # operation 20
  ['MUL'],
  ['LOADZ', 9],
  ['LOADZ', 11],
  ['STORE', 11],
  # operation 21
  ['MUL'],
  ['LOAD_DATA'],
  ['LOAD', 11],
  ['STORE', 12],
  # operation 22
  ['ADD'],
  ['LOADZ', 12],
  ['LOADZ', 13],
  ['STORE', 13],
  # operation 23
  ['SUB'],
  ['LOADZ', 10],
  ['LOAD', 1],
  ['STORE', 10],
  # branch if non-zero to operation 13
  ['BRN', -45],
  # operation 24
  ['SUB'],
  ['LOAD', 0],
  ['LOADZ', 13],
  # print
  ['PRINT'],
  # operation 25
  ['ADD'],
  ['LOAD', 1],
  ['LOADZ', 3],
  ['STORE', 3],
  # reset working variables
  ['SET', 6, 0],
  ['SET', 7, 0],
  ['SET', 11, 0], # stops overwrite warnings
  # end
  ['HALT'],
])

# indices B[k]
k = 1
# input data, initially empty, but each result is added after computation
data = []
# instruction to start execution at, initially 0, but subsequently 4
start = 0
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
  start = 4
  k += 2
