from errno import EINVAL
import typing

from sparse import SparseReadMode
from sparse_file import SparseFile

def _do_sparse_file_read_normal(s: SparseFile, fd: typing.BinaryIO, offset: int,
                                remain: int) -> int:
  block = offset // s.block_size

  while remain > 0:
    to_read = min(remain, s.block_size)
    # TBD

    if to_read == s.block_size:
      sparse_block = True
      # TBD
    else:
      sparse_block = False

    # TBD

    remain -= to_read
    offset += to_read
    block += 1

  return 0

def _sparse_file_read_normal(s: SparseFile, fd: typing.BinaryIO) -> int:
  ret = _do_sparse_file_read_normal(s, fd, 0, s.len_)
  return ret

def sparse_file_read(s: SparseFile, fd: typing.BinaryIO, mode: SparseReadMode) -> int:
  match mode:
    case SparseReadMode.NORMAL:
      return _sparse_file_read_normal(s, fd)
    case _:
      return -EINVAL
