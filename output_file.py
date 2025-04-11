"""
  core/libsparse/output_file.h
  core/libsparse/output_file.cpp
"""

import dataclasses
from errno import EINVAL, ENOMEM
import typing

from sparse_defs import error_errno

from c_style_macros import py_pass_func_name
from py_reserved_mem import g_reserved_mem

@dataclasses.dataclass
class OutputFile:
  # TBD
  _chunk_cnt: int = 0
  # TBD
  _block_size: int = 0
  _len: int = 0

@dataclasses.dataclass
class OutputFileNormal:
  out: OutputFile = dataclasses.field(default_factory=OutputFile)
  fd: typing.Optional[typing.BinaryIO] = None

def read_all(fd: typing.BinaryIO, len_: int) -> tuple[int, typing.Optional[bytes]]:
  try:
    # Python: EINTR is alr handled by stdlib
    buf = fd.read(len_)
  except MemoryError:
    # Python-specific
    g_reserved_mem.release()
    return (-ENOMEM, None)
  except OSError as e:
    return (-e.errno, None)

  if len(buf) != len_:
    return (-EINVAL, None)

  return (0, buf)

def _output_file_init(out: OutputFile, block_size: int, len_: int,
                      chunks: int) -> int:
  out._len = len_
  out._block_size = block_size
  # TBD
  out._chunk_cnt = chunks

  # TBD

  return 0

@py_pass_func_name
def _output_file_new_normal(func__: str) -> typing.Optional[OutputFile]:
  try:
    outn = OutputFileNormal()
  except MemoryError:
    g_reserved_mem.release()
    error_errno(func__, ENOMEM, "malloc struct outn")
    return None

  # TBD

  return outn.out

def output_file_open_fd(fd: typing.BinaryIO, block_size: int, len_: int,
                        chunks: int) -> typing.Optional[OutputFile]:
  out = _output_file_new_normal()
  if out is None:
    return None

  # TBD

  ret = _output_file_init(out, block_size, len_, chunks)
  if ret < 0:
    return None

  return out
