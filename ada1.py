#!/usr/bin/env python -t
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# https://enigmaticcode.wordpress.com/2015/09/24/running-the-first-program/
# Program 1 - ada1.py

from fractions import Fraction

# my implementation of the algorithm
def bernoulli():

  # results
  Bs = list()

  # start at n=1
  n = 1
  # calculate the sequence
  while True:

    # result = A0
    r = -Fraction(2 * n - 1, 2 * n + 1) / 2

    # A1 = n
    A = n
    # for each B[k] already determined calculate the corresponding A[k]
    for (i, B) in enumerate(Bs):
      if i > 0:
        # multiply in the 2 additional terms
        j = 2 * i - 1
        A *= Fraction(2 * n - j, 2 + j)
        j += 1
        A *= Fraction(2 * n - j, 2 + j)
      # add A[k] * B[k] into the result
      r += A * B

    # the computed bernoulli number is -r
    B = -r
    # return the number
    yield B
    # add it to the result list
    Bs.append(B)
    # increase n
    n += 1


# run N iterations of the algorithm
from sys import argv
N = (10 if len(argv) < 2 else int(argv[1]))

k = 1 # ada's numbering (normal numbering is k + 1)
K = 2 * N + 1 # max k
for r in bernoulli():
  print("B[{k}] = {r}".format(k=k, r=r))
  k += 2
  if k == K: break
