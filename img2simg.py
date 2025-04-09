"""
  core/libsparse/img2simg.cpp
"""

import getopt
from getopt import gnu_getopt
from os import SEEK_SET, SEEK_END, strerror
import sys
from sys import stderr

from sparse import (SparseReadMode, sparse_file_new,
                    sparse_file_destroy, sparse_file_verbose)
from sparse_read import sparse_file_read

from py_reserved_mem import g_reserved_mem

def usage():
  print("Usage: img2simg.py <raw_image_file> <sparse_image_file>", file=stderr)

def main(argv: list[str]) -> int:
  # XXX(Python)
  if not g_reserved_mem.acquire(0x10000):
    stderr.write('Cannot allocate 64K reserved memory\n')
    return 1

  mode = SparseReadMode.NORMAL
  block_size = 4096

  try:
    _, args = gnu_getopt(argv[1:], "", [])
  except getopt.GetoptError as e:
    print(f'{argv[0]}: {e}', file=stderr)
    usage()
    return 1

  if len(args) != 2:
    usage()
    return 1

  arg_in = args[0]
  try:
    in_ = open(arg_in, 'rb')
  except OSError as e:
    print("Cannot open input file %s: %s" % (arg_in, e.strerror), file=stderr)
    return 1

  arg_out = args[1]
  try:
    out = open(arg_out, 'wb')
  except OSError as e:
    print("Cannot open output file %s: %s" % (arg_out, e.strerror), file=stderr)
    return 1

  len_ = in_.seek(0, SEEK_END)
  in_.seek(0, SEEK_SET)

  s = sparse_file_new(block_size, len_)
  if s is None:
    print("Failed to create sparse file", file=stderr)
    return 1

  sparse_file_verbose(s)
  ret = sparse_file_read(s, in_, mode)
  if ret < 0:
    print("Failed to read file: %s" % strerror(-ret), file=stderr)
    return 1

  # TBD

  sparse_file_destroy(s)

  in_.close()
  out.close()

  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
