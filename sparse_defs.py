"""
  core/libsparse/sparse_defs.h
"""

from os import strerror
from sys import stderr

def error(func__: str, fmt: str, *args):
  print(("error: %s: " + fmt) % (func__, *args), file=stderr)

def error_errno(func__: str, errno: int, s: str, *args):
  error(func__, s + ": %s", *args, strerror(errno))
