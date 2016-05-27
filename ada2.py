#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/09/24/running-the-first-program/
# Program 2 - ada2.py

from collections import defaultdict
from fractions import Fraction

# ada lovelace's algorithm in Python
def bernoulli():

  # initially all varibles in the store are at 0
  v = defaultdict(int)

  # program start

  # initialise the variables
  v[1] = Fraction(1) # constant
  v[2] = Fraction(2) # constant
  v[3] = Fraction(1) # n = 1

  # outer loop (compute B[2n - 1])
  while True:

    # pseudo-block to permit "break"
    while True:

      # 0: set index register
      i = 1

      # 1: v4 = v5 = v6 = 2n
      v[4] = v[5] = v[6] = v[2] * v[3]

      # 2: v4 = 2n - 1
      v[4] = v[4] - v[1]

      # 3: v5 = 2n + 1
      v[5] = v[5] + v[1]

      # 4: v11 = (2n - 1)/(2n + 1) (the diagram seems to say v[5] / v[4]) [FIX]
      v[11] = v[4] / v[5]

      # 5: v11 = (1/2) (2n - 1)/(2n + 1)
      v[11] = v[11] / v[2]

      # 6: v13 = -(1/2) (2n - 1)/(2n + 1) = A0
      v[13] = v[13] - v[11]

      # 7: v10 = n - 1
      v[10] = v[3] - v[1]
      # branch if zero to operation 24
      if v[10] == 0: break

      # 8: v7 = 2
      v[7] = v[2] + v[7]

      # 9: v11 = (2n)/2 = A1 [why not just set v[11] = v[3] instead of 8 & 9]
      v[11] = v[6] / v[7]

      # 10: v12 = A1 * B1
      v[12] = v[20 + i] * v[11]
      i = i + 1

      # 11: v13 = A0 + A1 * B1
      v[13] = v[12] + v[13]

      # 12: v10 = n - 2
      v[10] = v[10] - v[1]
      # branch if zero to operation 24
      if v[10] == 0: break

      # for each computed result, B = B3 [1], B5 [2], ...
      while True:

        # 13: v6 = 2n - 1 [1], 2n - 3 [2], ...
        v[6] = v[6] - v[1]

        # 14: v7 = 3 [1], 5 [2], ...
        v[7] = v[1] + v[7]

        # 15: v8 = (2n - 1)/3 [1], (2n - 3)/5 [2], ...
        v[8] = v[6] / v[7]

        # 16: v11 = (2n)/2 * (2n - 1)/3 [1], (2n)/2 * (2n - 1)/3 * (2n - 3)/5 [2], ...
        v[11] = v[8] * v[11]

        # 17: v6 = 2n - 2 [1], 2n - 4 [2], ...
        v[6] = v[6] - v[1]

        # 18: v7 = 4 [1], 6 [2], ...
        v[7] = v[1] + v[7]

        # 19: v9 = (2n - 2)/4 [1], (2n - 4)/6
        v[9] = v[6] / v[7]

        # 20: v11 = (2n)/2 * (2n - 1)/3 * (2n - 2)/4 = A3 [1], (2n)/2 * (2n - 1)/3 * (2n - 2)/4 * (2n - 3)/5 * (2n - 4)/6 = A5 [2], ... 
        v[11] = v[9] * v[11]

        # 21: v12 = A3 * B3 [1], A5 * B5 [2], ...
        v[12] = v[20 + i] * v[11]
        i = i + 1

        # 22: v13 = A0 + A1 * B1 + A3 * B3 [1], A0 + A1 * B1 + A3 * B3 + A5 * B5 [2], ...
        v[13] = v[12] + v[13]

        # 23: v10 = n - 3 [1], n - 4 [2], ...
        v[10] = v[10] - v[1]
        # branch if non-zero to operation 13
        if v[10] == 0: break

      # terminate the pseudo-block
      break

    # 24: result (-v13) is copied into the results
    r = v[20 + i] = v[20 + i] - v[13]

    # the result could be printed here
    # we pass it back to the calling routine
    yield r

    # 25: increase n, and reset working variables
    v[3] = v[1] + v[3]
    v[7] = v[13] = 0

    # branch to operation 0


# run N iterations of the algorithm
N = 10

# allow N to be specified as a command line argument
import sys
if len(sys.argv) > 1:
  N = int(sys.argv[1])

k = 1 # ada's numbering (normal numbering is k + 1)
K = 2 * N + 1 # max k
for r in bernoulli():
  print("B[{k}] = {r}".format(k=k, r=r))
  k += 2
  if k == K: break
