"""
  core/libsparse/sparse_file.h
"""

import dataclasses
import typing

from backed_block import BackedBlockList

@dataclasses.dataclass
class SparseFile:
  block_size: int = 0
  len_: int = 0
  verbose: bool = False

  backed_block_list: typing.Optional[BackedBlockList] = None
