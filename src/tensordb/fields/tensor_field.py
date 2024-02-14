
import numpy as np
from dataclasses import dataclass


@dataclass
class TensorField:
    """Dataclass to define a TensorField."""
    dtype: np.dtype
    shape: None | tuple[int | None, ...]