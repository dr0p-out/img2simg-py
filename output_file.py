from errno import EINVAL, ENOMEM
import typing

from py_reserved_mem import g_reserved_mem

def read_all(fd: typing.BinaryIO, len_: int) -> tuple[int, typing.Optional[bytes]]:
  try:
    buf = fd.read(len_)
  except MemoryError:
    g_reserved_mem.release()
    return (-ENOMEM, None)
  except OSError as e:
    return (-e.errno, None)

  if len(buf) != len_:
    return (-EINVAL, None)

  return (0, buf)
