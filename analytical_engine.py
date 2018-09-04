#!/usr/bin/env python -t
###############################################################################
#
# File:         analytical_engine.py
# RCS:          $Header: $
# Description:  An Emulator for Babbage's Analytical Engine
# Author:       Jim Randell
# Created:      Wed Oct 12 08:51:22 2015
# Modified:     Fri Aug 31 14:01:11 2018 (Jim Randell) jim.randell@gmail.com
# Language:     Python
# Package:      N/A
# Status:       Experimental (Do Not Distribute)
#
# (C) Copyright 2015, Jim Randell, all rights reserved.
#
###############################################################################
# -*- mode: Python; py-indent-offset: 2; -*-

#
# See the articles on "Running the first program" at:
#
# Part 1: https://enigmaticcode.wordpress.com/2015/09/24/running-the-first-program/
# Part 2: https://enigmaticcode.wordpress.com/2015/10/14/running-the-first-program-part-2/
# Part 3: https://enigmaticcode.wordpress.com/2015/10/21/running-the-first-program-part-3/
#

from __future__ import print_function

__author__ = "Jim Randell <jim.randel@gmail.com>"
__version__ = "2018-08-26"

###############################################################################

# implementation of the columns in the Analytical Engine

from fractions import Fraction

class OverflowException(Exception): pass

# a column with <digits> whole decimal digits and <dp> fractional decimal digits
def Column(digits=50, dp=0):

  shift = (10 ** dp)
  overflow = (10 ** (digits + dp)) - 1
  fmt = '<{s}{m:0' + str(digits) + 'd}' + ('.{d:0' + str(dp) + 'd}' if dp > 0 else '') + '>'

  class Column(object):

    # create a value, and check for overflow
    def __init__(self, n=0, shift=shift):
      n = int(Fraction(n) * shift)
      if abs(n) > overflow:
        raise OverflowException("Overflow in column")
      self.n = n

    # output format
    def __repr__(self):
      n = self.n
      (m, d) = divmod(abs(n), shift)
      s = ('-' if n < 0 else '+')
      return fmt.format(s=s, m=m, d=d)

    # arithmetic operations

    def __add__(self, value):
      return Column(self.n + value.n, shift=1)

    def __sub__(self, value):
      return Column(self.n - value.n, shift=1)

    def __mul__(self, value):
      return Column((self.n * value.n) // shift, shift=1)

    def __div__(self, value):
      return Column((self.n * shift) // value.n, shift=1)

    # Python 3 uses __truediv__
    __truediv__ = __div__

    # branch tests

    def __eq__(self, value):
      return self.n == value.n

    def __ne__(self, value):
      return self.n != value.n

    def __lt__(self, value):
      return self.n < value.n

  return Column

# default column size
_column = Column(digits=10, dp=40)

###############################################################################

# emulation of the Analytical Engine

class HaltException(Exception): pass

class AnalyticalEngine(object):

  # vars = number of variables
  # number = a function to implement the variables
  # trace = trace flag

  def __init__(self, **kw):
    # number of variables in the store
    self.vars = 20
    # a method to implement the variables
    self.number = _column
    # trace flag
    self.trace = False
    # enable warnings?
    self.warn = False

    # set options
    for (k, v) in kw.items():
      if hasattr(self, k):
        setattr(self, k, v)
      else:
        print('AnalyticalEngine: ignoring "{k}={v}"'.format(k=k, v=v))
    
    self.reset()

  # reset the machine
  def reset(self):
    # representation of zero
    self.zero = self.number(0)
    # the variables in the store
    self.v = [self.zero] * self.vars
    # the registers in the mill
    self.index = 0
    self.input = [None, None]
    self.result = None
    # current operation
    self.op = None
    # the program and program counter
    self.program = None
    self.pc = None
    # input data
    self.data = None
    self.dc = None
    # output transcript
    self.output = None

  # load the program
  def load_program(self, program):
    self.program = program
    self.pc = 0
    if self.trace:
      print(">>> Loaded program cards:")
      if program:
        for (i, s) in enumerate(program):
          print("{i:3d}: {s}".format(i=i, s=s))
      else:
        print("[none]")

  # load the data
  def load_data(self, data):
    self.data = data
    self.dc = 0
    if self.trace:
      print(">>> Loaded data cards:")
      if data:
        for (i, s) in enumerate(data):
          print("{i:3d}: {s}".format(i=i, s=s))
      else:
        print("[none]")

  # run the program (starting at instruction start)
  def run(self, start=0):
    print(">>> Running Analytical Engine [version: {v}]".format(v=__version__))
    stats = dict()
    self.output = []
    self.pc = start
    try:

      while True:
        # get the next instruction
        assert not(self.pc < 0), "Invalid PC"
        p = self.program[self.pc]
        self.pc += 1
        # execute it
        getattr(self, p[0])(*p[1:])
        # record stats
        if p[0] in stats:
          stats[p[0]] += 1
        else:
          stats[p[0]] = 1

    except Exception as e:
      print(">>> {e}".format(e=e))
      print(">>> Execution halted")

    if self.trace: print(">>> Stats: {stats}".format(stats=stats))
    self.stats = stats

  # implement the opcodes

  # SET <i> <x>
  # set variable <i> in the store to value <x>
  def SET(self, i, x):
    if self.trace: print(": SET v[{i}] <- {x}".format(i=i, x=x))
    self.v[i] = self.number(x)

  # ADD
  # set the engine to perform addition
  def ADD(self):
    if self.trace: print(": ADD")
    self.op = (lambda a, b: a + b)

  # SUB
  # set the engine to perform subtraction
  def SUB(self):
    if self.trace: print(": SUB")
    self.op = (lambda a, b: a - b)

  # MUL
  # set the engine to peform multiplication
  def MUL(self):
    if self.trace: print(": MUL")
    self.op = (lambda a, b: a * b)

  # DIV
  # set the engine to perform division
  def DIV(self):
    if self.trace: print(": DIV")    
    self.op = (lambda a, b: a / b)

  # execute an operation
  def _execute(self):
    self.result = self.op(self.input[0], self.input[1])

  # load value v into the input register
  def _load(self, v):
    self.input[self.index] = v
    # loading the second register triggers the execution
    if self.index == 1:
      if self.trace: print(": -> EXECUTE")
      self._execute()
      if self.trace: print(": -> RESULT = {result}".format(result=self.result))
    # next time load the other input register
    self.index ^= 1

  # LOAD <i>
  # load the input register from variable <i> in the store, keeping the value in the variable
  def LOAD(self, i):
    v = self.v[i]
    if self.trace: print(": LOAD i[{index}] <- v[{i}] = {v}".format(index=self.index, i=i, v=v))
    self._load(v)

  # LOADZ <i>
  # load the input register from variable <i> in the store, and zero the variable
  def LOADZ(self, i):
    v = self.v[i]
    self.v[i] = self.zero # destructive read
    if self.trace: print(": LOADZ i[{index}] <- v[{i}] = {v}".format(index=self.index, i=i, v=v))
    self._load(v)

  # LOAD_DATA
  # load the input register from next value in the input data stack
  def LOAD_DATA(self):
    v = self.data[self.dc]
    if self.trace: print(": LOAD_DATA i[{index}] <- {v}".format(index=self.index, v=v))
    self._load(v)
    self.dc += 1

  # STORE <i>
  # store the result to variable <i> in the store
  # TODO: the AE may have required that the current value was zero
  def STORE(self, i):
    if self.trace: print(": STORE v[{i}] <- {result}".format(i=i, result=self.result))
    if self.warn and self.v[i] != self.zero: print(">>> WARNING: STORE to non-zero variable, v[{i}] = {v}".format(i=i, v=self.v[i]))
    self.v[i] = self.result

  # PRINT
  # print the result
  def PRINT(self):
    if self.trace: print(": PRINT {result}".format(result=self.result))
    print(self.result)
    self.output.append(self.result)

  # HALT
  # halt execution of the engine
  def HALT(self):
    if self.trace: print(": HALT")
    raise HaltException("HALT instruction encountered")

  # branch
  def _branch(self, offset):
    if self.trace: print(": -> pc <- {pc} + {offset}".format(pc=self.pc, offset=offset))
    self.pc += offset

  # BRZ <offset>
  # branch if zero:
  # if the result is zero move the program instructions by <offset>
  def BRZ(self, offset):
    if self.trace: print(": BRZ {offset}".format(offset=offset))
    if self.result == self.zero:
      self._branch(offset)

  # BRN <offset>
  # branch if non-zero:
  # if the result is non-zero move the program instructions by <offset>
  def BRN(self, offset):
    if self.trace: print(": BRN {offset}".format(offset=offset))
    if self.result != self.zero:
      self._branch(offset)

  # BRA <offset>
  # branch always:
  # move the program instructions by <offset>
  def BRA(self, offset):
    if self.trace: print(": BRA {offset}".format(offset=offset))
    self._branch(offset)

  # BRP <offset>
  # branch if positive (plus):
  # if the result is positive move the program instructions by <offset>
  def BRP(self, offset):
    if self.trace: print(": BRP {offset}".format(offset=offset))
    if self.result > self.zero:
      self._branch(offset)

  # BRM <offset>
  # branch if negative (minus):
  # if the result is negative move the program instructions by <offset>
  def BRM(self, offset):
    if self.trace: print(": BRM {offset}".format(offset=offset))
    if self.result < self.zero:
      self._branch(offset)

  # assemble a program
  def assemble(self, ss):
    return assemble(ss)

###############################################################################

# an assembler for the Analytical Engine

# the assembler
def assemble(ss):

  # split a line into tokens
  def tokenise(s):
    for t in s.split():
      # drop syntactic sugar
      if t in ('->', '<-'): continue
      # turn numbers into ints
      v = t.startswith('v') # variable indices may be optionally prefixed with 'v'
      try:
        if t.endswith('.'):
          # trailing '.' = destructive read, use a negative value index
          yield -(int(t[v:-1:]) + 1)
        else:
          # non-destructive read, use a normal index
          yield int(t[v:])
      except ValueError:
        yield t

  # parse the program into tokens
  def parse(ss):
    for s in ss.splitlines():
      # strip comments
      i = s.find('#')
      if i > -1:
        s = s[:i]
      # strip whitespace
      s = s.strip()
      # skip empty lines
      if not s: continue
      # split into tokens
      yield list(tokenise(s))

  program = []
  labels = dict()

  # pass 1:
  # - parse the input
  # - generate the cards
  # - record the labels
  for s in parse(ss):
    # consider the first token in a line
    s0 = s[0]
    if s0.startswith(':'):
      # :<label>
      labels[s0[1:]] = len(program)
    elif s0 in ('ADD', 'SUB', 'MUL', 'DIV'):
      # <op> <load1> <load2> [<store> ...]
      program.append([s0])
      for v in s[1:3]:
        if v == 'DATA':
          # special token DATA is used to load input data
          program.append(['LOAD_DATA'])
        else:
          # otherwise load from the store
          if v < 0:
            # negative indices indicate destructive reads
            program.append(['LOADZ', -(v + 1)])
          else:
            # non-destructive read
            program.append(['LOAD', v])
      for v in s[3:]:
        assert not(v < 0), "invalid STORE"
        program.append(['STORE', v])
    else:
      # everything else
      program.append(s)

  # pass 2:
  # - calculate branches in the program
  for (i, s) in enumerate(program):
    if s[0].startswith('BR'): # ('BRZ', 'BRN', 'BRA')
      # <branch> <offset>
      if isinstance(s[1], str):
        # only replace symbolic (string) labels
        s[1] = labels[s[1]] - (i + 1)

  # return the program cards, and the addresses of the labels
  return (program, labels)
