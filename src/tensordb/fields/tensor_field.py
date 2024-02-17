from dataclasses import dataclass

import numpy as np


@dataclass
class TensorField:
    """Dataclass to define a TensorField."""

    dtype: np.dtype
    shape: None | tuple[int | None, ...]
