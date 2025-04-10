"""
  core/libsparse/backed_block.h
  core/libsparse/backed_block.cpp
"""

from __future__ import annotations

import dataclasses
from errno import EINVAL, ENOMEM
import typing

from sparse_defs import align_down

from py_reserved_mem import g_reserved_mem

@dataclasses.dataclass
class BackedBlock:
  _block: int = 0
  _len: int = 0
  _next: typing.Optional[BackedBlock] = None
  # Python: union fields are in sub-classes

@dataclasses.dataclass
class BackedBlockFd(BackedBlock):
  _fd: typing.Optional[typing.BinaryIO] = None
  _offset: int = 0

@dataclasses.dataclass
class BackedBlockFill(BackedBlock):
  _val: int = 0

@dataclasses.dataclass
class BackedBlockList:
  _data_blocks: typing.Optional[BackedBlock] = None
  _last_used: typing.Optional[BackedBlock] = None
  _block_size: int = 0

def backed_block_iter_new(bbl: BackedBlockList) -> typing.Optional[BackedBlock]:
  return bbl._data_blocks

def backed_block_iter_next(bb: BackedBlock) -> typing.Optional[BackedBlock]:
  return bb._next

def backed_block_iter(bbl: BackedBlockList) -> typing.Generator[BackedBlock, None, None]:
  bb = backed_block_iter_new(bbl)
  while bb is not None:
    yield bb
    bb = backed_block_iter_next(bb)

def backed_block_len(bb: BackedBlock) -> int:
  return bb._len

def backed_block_block(bb: BackedBlock) -> int:
  return bb._block

def backed_block_destroy(bb: BackedBlock):
  pass  # Python: no-op for now

def backed_block_list_new(block_size: int) -> typing.Optional[BackedBlockList]:
  try:
    b = BackedBlockList()
  except MemoryError:
    g_reserved_mem.release()
    return None
  b._block_size = block_size
  return b

def backed_block_list_destroy(bbl: BackedBlockList):
  if bbl._data_blocks is not None:
    bb = bbl._data_blocks
    while bb is not None:
      next_ = bb._next
      backed_block_destroy(bb)
      bb = next_

def _merge_bb(bbl: BackedBlockList, a: typing.Optional[BackedBlock], b: typing.Optional[BackedBlock]) -> int:
  if a is None or b is None:
    return -EINVAL

  assert a._block < b._block

  if type(a) is not type(b):
    return -EINVAL

  block_len = a._len // bbl._block_size
  if a._block + block_len != b._block:
    return -EINVAL

  # TODO(Python): use match stmt
  if isinstance(a, BackedBlockFill):
    if a._val != b._val:
      return -EINVAL
  elif isinstance(a, BackedBlockFd):
    if a._fd is not b._fd or a._offset + a._len != b._offset:
      return -EINVAL

  a._len += b._len
  a._next = b._next

  backed_block_destroy(b)

  return 0

def _queue_bb(bbl: BackedBlockList, new_bb: BackedBlock) -> int:
  if bbl._data_blocks is None:
    bbl._data_blocks = new_bb
    return 0

  if bbl._data_blocks._block > new_bb._block:
    new_bb._next = bbl._data_blocks
    bbl._data_blocks = new_bb
    return 0

  if bbl._last_used is not None and new_bb._block > bbl._last_used._block:
    bb = bbl._last_used
  else:
    bb = bbl._data_blocks
  bbl._last_used = new_bb

  while bb._next is not None and bb._next._block < new_bb._block:
    bb = bb._next

  if bb._next is None:
    bb._next = new_bb
  else:
    new_bb._next = bb._next
    bb._next = new_bb

  _merge_bb(bbl, new_bb, new_bb._next)
  if _merge_bb(bbl, bb, new_bb) == 0:
    bbl._last_used = bb

  return 0

def backed_block_add_fill(bbl: BackedBlockList, fill_val: int, len_: int,
                          block: int) -> int:
  try:
    bb = BackedBlockFill()
  except MemoryError:
    g_reserved_mem.release()
    return -ENOMEM

  bb._block = block
  bb._len = len_
  bb._val = fill_val
  bb._next = None

  return _queue_bb(bbl, bb)

def backed_block_add_fd(bbl: BackedBlockList, fd: typing.BinaryIO, offset: int, len_: int,
                        block: int) -> int:
  try:
    bb = BackedBlockFd()
  except MemoryError:
    g_reserved_mem.release()
    return -ENOMEM

  bb._block = block
  bb._len = len_
  bb._fd = fd
  bb._offset = offset
  bb._next = None

  return _queue_bb(bbl, bb)

def backed_block_split(bbl: BackedBlockList, bb: BackedBlock,
                       max_len: int) -> int:
  max_len = align_down(max_len, bbl._block_size)

  if bb._len <= max_len:
    return 0

  try:
    new_bb = dataclasses.replace(bb)  # Python: same type as bb
  except MemoryError:
    g_reserved_mem.release()
    return -ENOMEM

  # Python: values are already copied

  new_bb._len = bb._len - max_len
  new_bb._block = bb._block + max_len // bbl._block_size
  new_bb._next = bb._next

  # TODO(Python): use match stmt
  if isinstance(bb, BackedBlockFd):
    new_bb._offset += max_len
  elif isinstance(bb, BackedBlockFill):
   pass

  bb._next = new_bb
  bb._len = max_len
  return 0
