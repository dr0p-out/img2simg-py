import enum
import typing

from sparse_file import SparseFile
from backed_block import backed_block_list_new

class SparseReadMode(enum.Enum):
  NORMAL = enum.auto()

def sparse_file_new(block_size: int, len_: int) -> typing.Optional[SparseFile]:
  try:
    s = SparseFile()
  except MemoryError:
    return None

  s.backed_block_list = backed_block_list_new(block_size)
  if s.backed_block_list is None:
    return None

  s.block_size = block_size
  s.len_ = len_

  return s
