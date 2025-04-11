"""
  core/libsparse/include/sparse/sparse.h
  core/libsparse/sparse.cpp
"""

from errno import ENOMEM
import enum
import typing

from sparse_file import SparseFile
from backed_block import (backed_block_iter, backed_block_len,
                          backed_block_block, backed_block_list_new,
                          backed_block_list_destroy, backed_block_add_fill,
                          backed_block_add_fd, backed_block_split)
from output_file import OutputFile, output_file_open_fd
from sparse_defs import div_round_up

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

def sparse_file_destroy(s: SparseFile):
  backed_block_list_destroy(s.backed_block_list)

def sparse_file_add_fill(s: SparseFile, fill_val: int, len_: int,
                         block: int) -> int:
  return backed_block_add_fill(s.backed_block_list, fill_val, len_, block)

def sparse_file_add_fd(s: SparseFile, fd: typing.BinaryIO, file_offset: int, len_: int,
                       block: int) -> int:
  return backed_block_add_fd(s.backed_block_list, fd, file_offset, len_, block)

def sparse_count_chunks(s: SparseFile) -> int:
  last_block = 0
  chunks = 0

  for bb in backed_block_iter(s.backed_block_list):
    if backed_block_block(bb) > last_block:
      chunks += 1
    chunks += 1
    last_block = backed_block_block(bb) + div_round_up(backed_block_len(bb), s.block_size)
  if last_block < div_round_up(s.len_, s.block_size):
    chunks += 1

  return chunks

_MAX_BACKED_BLOCK_SIZE = 64 << 20

def _write_all_blocks(s: SparseFile, out: OutputFile) -> int:
  last_block = 0

  for bb in backed_block_iter(s.backed_block_list):
    if backed_block_block(bb) > last_block:
      blocks = backed_block_block(bb) - last_block
      # TBD
    # TBD
    last_block = backed_block_block(bb) + div_round_up(backed_block_len(bb), s.block_size)

  pad = s.len_ - last_block * s.block_size
  assert pad >= 0
  # TBD

  return 0

def sparse_file_write(s: SparseFile, fd: typing.BinaryIO) -> int:
  for bb in backed_block_iter(s.backed_block_list):
    ret = backed_block_split(s.backed_block_list, bb, _MAX_BACKED_BLOCK_SIZE)
    if ret < 0:
      return ret

  chunks = sparse_count_chunks(s)
  out = output_file_open_fd(fd, s.block_size, s.len_, chunks)

  if out is None: return -ENOMEM

  ret = _write_all_blocks(s, out)

  # TBD

  return ret

def sparse_file_verbose(s: SparseFile):
  s.verbose = True
