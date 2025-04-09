"""
  core/libsparse/include/sparse/sparse.h
  core/libsparse/sparse.cpp
"""

import enum
import typing

from sparse_file import SparseFile
from backed_block import backed_block_list_new, backed_block_add_fill

from py_reserved_mem import g_reserved_mem

class SparseReadMode(enum.Enum):
  NORMAL = enum.auto()

def sparse_file_new(block_size: int, len_: int) -> typing.Optional[SparseFile]:
  try:
    s = SparseFile()
  except MemoryError:
    g_reserved_mem.release()
    return None

  s.backed_block_list = backed_block_list_new(block_size)
  if s.backed_block_list is None:
    return None

  s.block_size = block_size
  s.len_ = len_

  return s

def sparse_file_add_fill(s: SparseFile, fill_val: bytes, len_: int,
                         block: int) -> int:
  return backed_block_add_fill(s.backed_block_list, fill_val, len_, block)

def sparse_file_verbose(s: SparseFile):
  s.verbose = True
