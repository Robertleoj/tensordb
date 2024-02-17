#!/usr/bin/env python3

"""A script to build the C++ backend and install the bindings into the source tree."""

import os
import shutil
import subprocess
from functools import partial
from pathlib import Path

from fire import Fire
from generate_config import build_config

BUILD_DIR = "build"

PACKAGE_NAME = "tensordb"
CPP_PACKAGE_NAME = "_tensordb_cpp"
MODULE_NAME = f"{CPP_PACKAGE_NAME}.cpython-310-x86_64-linux-gnu.so"


def check_in_repo() -> None:
    """Check that we are executing this from repo root."""
    assert Path("pyproject.toml").exists(), "This command should run in repo root."


def build(debug: bool = False) -> None:
    """(Re)build the C++ backend."""
    check_in_repo()
    build_config()

    build_path = Path("build")
    build_path.mkdir(exist_ok=True)

    cmake_cmd = ["cmake", "-B", str(build_path)]
    if debug:
        cmake_cmd += ["-DCMAKE_BUILD_TYPE=Debug"]

    cmake_cmd += ["-G", "Ninja"]

    subprocess.run(cmake_cmd, check=True)

    subprocess.run(["ninja", "-C", str(build_path)])

    # Make sure that target was built
    target_path = build_path / "src" / PACKAGE_NAME / CPP_PACKAGE_NAME / MODULE_NAME
    print(target_path)
    assert target_path.exists()

    # Replace or create symlink
    deploy_path = Path("src") / PACKAGE_NAME / MODULE_NAME
    if deploy_path.is_symlink():
        deploy_path.unlink()

    deploy_path.symlink_to(target_path.resolve())

    subprocess.run(
        ["stubgen", "-p", CPP_PACKAGE_NAME, "-o", f"./src/{PACKAGE_NAME}", "--include-docstring"],
        env=dict(os.environ, PYTHONPATH=f"./src/{PACKAGE_NAME}"),
    )


def clean() -> None:
    """Clean the build folder and remove the symlink, if any."""
    check_in_repo()
    shutil.rmtree(BUILD_DIR, ignore_errors=True)

    # Remove the symlink, if any
    deploy_path = Path(f"src/{PACKAGE_NAME}/{MODULE_NAME}")
    if deploy_path.is_symlink():
        deploy_path.unlink()


def clean_build(debug: bool = False):
    """Clean the build folder and remove the symlink, if any."""
    clean()
    build(debug=debug)


if __name__ == "__main__":
    Fire(
        {
            "build": build,
            "build_debug": partial(build, debug=True),
            "clean": clean,
            "clean_build": clean_build,
            "clean_build_debug": partial(clean_build, debug=True),
        }
    )
