import enum
import typing

from sparse_file import SparseFile

class SparseReadMode(enum.Enum):
  NORMAL = enum.auto()

def sparse_file_new(block_size: int, len_: int) -> typing.Optional[SparseFile]:
  try:
    s = SparseFile()
  except MemoryError:
    return None

  # TBD

  s.block_size = block_size
  s.len_ = len_

  return s
