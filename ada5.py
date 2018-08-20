#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/10/14/running-the-first-program-part-2/
# Program 4 - ada5.py

from analytical_engine import AnalyticalEngine
from fractions import Fraction
from enigma import raw_input, printf

# initialise the engine
p = AnalyticalEngine(vars=14, number=Fraction)

# load the program
p.load_program([
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
  ['LOAD', 4],
  ['LOAD', 1],
  ['STORE', 4],
  # operation 3
  ['ADD'],
  ['LOAD', 5],
  ['LOAD', 1],
  ['STORE', 5],
  # operation 4
  ['DIV'],
  ['LOAD', 4],
  ['LOAD', 5],
  ['STORE', 11],
  # operation 5
  ['DIV'],
  ['LOAD', 11],
  ['LOAD', 2],
  ['STORE', 11],
  # operation 6
  ['SUB'],
  ['LOAD', 13],
  ['LOAD', 11],
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
  ['LOAD', 7],
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
  ['LOAD', 12],
  ['LOAD', 13],
  ['STORE', 13],
  # operation 12
  ['SUB'],
  ['LOAD', 10],
  ['LOAD', 1],
  ['STORE', 10],
  # branch if zero to operation 24
  ['BRZ', +45],
  # operation 13
  ['SUB'],
  ['LOAD', 6],
  ['LOAD', 1],
  ['STORE', 6],
  # operation 14
  ['ADD'],
  ['LOAD', 1],
  ['LOAD', 7],
  ['STORE', 7],
  # operation 15
  ['DIV'],
  ['LOAD', 6],
  ['LOAD', 7],
  ['STORE', 8],
  # operation 16
  ['MUL'],
  ['LOAD', 8],
  ['LOAD', 11],
  ['STORE', 11],
  # operation 17
  ['SUB'],
  ['LOAD', 6],
  ['LOAD', 1],
  ['STORE', 6],
  # operation 18
  ['ADD'],
  ['LOAD', 1],
  ['LOAD', 7],
  ['STORE', 7],
  # operation 19
  ['DIV'],
  ['LOAD', 6],
  ['LOAD', 7],
  ['STORE', 9],
  # operation 20
  ['MUL'],
  ['LOAD', 9],
  ['LOAD', 11],
  ['STORE', 11],
  # operation 21
  ['MUL'],
  ['LOAD_DATA'],
  ['LOAD', 11],
  ['STORE', 12],
  # operation 22
  ['ADD'],
  ['LOAD', 12],
  ['LOAD', 13],
  ['STORE', 13],
  # operation 23
  ['SUB'],
  ['LOAD', 10],
  ['LOAD', 1],
  ['STORE', 10],
  # branch if non-zero to operation 13
  ['BRN', -45],
  # operation 24
  ['SUB'],
  ['LOAD', 0],
  ['LOAD', 13],
  # print
  ['PRINT'],
  # operation 25
  ['ADD'],
  ['LOAD', 1],
  ['LOAD', 3],
  ['STORE', 3],
  # reset working variables
  ['SET', 7, 0],
  ['SET', 13, 0],
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
  start = 4
  k += 2
