# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: tendordb-IeMUXgL4-py3.10
#     language: python
#     name: python3
# ---

# %%
import shutil
from pathlib import Path

import numpy as np
from tensordb._backend import Backend
from tensordb.fields import TensorField

# %%
p = Path("./data")
shutil.rmtree(str(p))
p.mkdir(exist_ok=True)

# %%
backend = Backend(p)

# %%
backend.create_collection(
    "test", fields={"name": str, "number": int, "tensor": TensorField(dtype=np.int32, shape=(None, 2))}
)

# %%
backend.get_collection_fields("test")
