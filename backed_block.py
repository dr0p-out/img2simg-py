from __future__ import annotations

import dataclasses
import typing

@dataclasses.dataclass
class BackedBlock:
  _block: int = 0
  _len: int = 0
  _next: typing.Optional[BackedBlock] = None

@dataclasses.dataclass
class BackedBlockList:
  _data_blocks: typing.Optional[BackedBlock] = None
  _last_used: typing.Optional[BackedBlock] = None
  _block_size: int = 0

def backed_block_list_new(block_size: int) -> typing.Optional[BackedBlockList]:
  try:
    b = BackedBlockList()
  except MemoryError:
    return None
  b._block_size = block_size
  return b
