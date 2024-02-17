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

from tensordb import Database

# %%
p = Path("../data")
shutil.rmtree(str(p), ignore_errors=True)
p.mkdir(exist_ok=True)

# %%
db = Database("test_db", p)

# %%
db.collections()

# %%
fields = {"name": str, "number": int}

# %%
coll = db.collection("test", fields=fields)

# %%
coll.insert({"name": "Boi", "number": 7})

# %%
coll.find().execute()

# %%
coll.insert(
    [
        {"name": "Eva", "number": 42},
        {"name": "Bob", "number": 420},
    ]
)

# %%
coll.find({"number": 42}).execute()

# %%
db.collections()
