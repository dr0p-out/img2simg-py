import dataclasses

@dataclasses.dataclass
class SparseFile:
  block_size: int = 0
  len_: int = 0
  verbose: bool = False

  # TBD
