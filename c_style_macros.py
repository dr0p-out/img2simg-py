"""
compiler built-in defines
"""

import types

def py_pass_func_name(func: types.FunctionType) -> ...:
  """
  __func__
  """
  def wrapper(*args, **kwargs) -> ...:
    return func(func.__name__, *args, **kwargs)
  return wrapper
