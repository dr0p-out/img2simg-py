"""
r/hacks
"""

import typing

class _ReservedMemory:
  def __init__(self):
    self._inner: typing.Optional[bytearray] = None

  def acquire(self, size: int) -> bool:
    try:
      self._inner = bytearray(size)
    except MemoryError:
      return False
    return True

  def release(self):
    self._inner = None

g_reserved_mem = _ReservedMemory()
