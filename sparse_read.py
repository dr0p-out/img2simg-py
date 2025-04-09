"""
  core/libsparse/include/sparse/sparse.h
  core/libsparse/sparse_read.cpp
"""

from errno import EINVAL, ENOMEM
import struct
import typing

from sparse import SparseReadMode, sparse_file_add_fill, sparse_file_add_fd
from output_file import read_all
from sparse_file import SparseFile
from sparse_defs import error_errno

from c_style_macros import py_pass_func_name
from py_reserved_mem import g_reserved_mem

@py_pass_func_name
def _do_sparse_file_read_normal(func__: str,
                                s: SparseFile, fd: typing.BinaryIO, offset: int,
                                remain: int) -> int:
  block = offset // s.block_size

  while remain > 0:
    to_read = min(remain, s.block_size)
    ret, buf = read_all(fd, to_read)
    if ret < 0:
      error_errno(func__, -ret, "failed to read sparse file")
      return ret

    if to_read == s.block_size:
      try:
        # XXX(Python): adapted for perf
        sparse_block = buf == buf[:4] * (s.block_size // 4)
      except MemoryError:
        g_reserved_mem.release()
        return -ENOMEM
    else:
      sparse_block = False

    if sparse_block:
      ret = sparse_file_add_fill(s, struct.unpack('<I', buf[:4])[0], to_read, block)
    else:
      ret = sparse_file_add_fd(s, fd, offset, to_read, block)

    if ret < 0:
      return ret

    remain -= to_read
    offset += to_read
    block += 1

  return 0

def _sparse_file_read_normal(s: SparseFile, fd: typing.BinaryIO) -> int:
  # Python: buf is allocated in read_all()
  ret = _do_sparse_file_read_normal(s, fd, 0, s.len_)
  return ret

def sparse_file_read(s: SparseFile, fd: typing.BinaryIO, mode: SparseReadMode) -> int:
  match mode:
    case SparseReadMode.NORMAL:
      return _sparse_file_read_normal(s, fd)
    case _:
      return -EINVAL
