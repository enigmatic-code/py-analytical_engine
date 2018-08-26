# This is a reduced version of the enigma.py library, sufficient to provide
# useful routines for the Analytical Engine programs.
#
# The full version is available at:
#
#   http://www.magwag.plus.com/jim/enigma.html

from __future__ import print_function

import sys

# provide: raw_input()

if sys.version_info[0] == 2:
  # Python 2.x
  raw_input = raw_input
elif sys.version_info[0] > 2:
  # Python 3.x
  raw_input = input

# provide: printf()

def update(s, ps=(), vs=None):
  if vs is not None: ps = zip(ps, vs)
  try:
    # use copy() method if available
    s = s.copy()
  except AttributeError:
    # otherwise create a new object initialised from the old one
    s = type(s)(s)
  try:
    # use update() method if available
    s.update(ps)
  except AttributeError:
    # otherwise update the pairs individually
    for (k, v) in ps:
      s[k] = v
  # return the new object
  return s

def _sprintf(fmt, vs, kw):
  if kw: vs = update(vs, kw)
  return fmt.format(**vs)

def printf(fmt='', **kw):
  s = _sprintf(fmt, sys._getframe(1).f_locals, kw)
  d = dict() # flush=1
  if s.endswith('\\'): (s, d['end']) = (s[:-1], '')
  print(s, **d)
