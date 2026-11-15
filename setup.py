"""
setup.py for GDAL Python bindings wheel build.

This file delegates all the heavy lifting to the system-installed GDAL
(via gdal-config on Linux/macOS, or GDAL_HOME env var on Windows).
"""
import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup


def get_gdal_config(option: str) -> str:
    """Call gdal-config and return its output (Linux / macOS)."""
    gdal_config = os.environ.get("GDAL_CONFIG", "gdal-config")
    result = subprocess.run(
        [gdal_config, f"--{option}"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def build_extension() -> Extension:
    platform = sys.platform

    if platform == "win32":
        # ── Windows ──────────────────────────────────────────────────────
        gdal_home = os.environ.get("GDAL_HOME", r"C:\vcpkg\installed\x64-windows")
        include_dirs = [
            os.path.join(gdal_home, "include"),
        ]
        library_dirs = [
            os.path.join(gdal_home, "lib"),
        ]
        libraries = ["gdal_i"]          # import lib on Windows
        extra_compile_args: list[str] = []
        extra_link_args: list[str] = []

    else:
        # ── Linux / macOS ─────────────────────────────────────────────────
        cflags = get_gdal_config("cflags")
        libs   = get_gdal_config("libs")

        include_dirs = [
            p[2:] for p in cflags.split() if p.startswith("-I")
        ]
        library_dirs = [
            p[2:] for p in libs.split()   if p.startswith("-L")
        ]
        libraries = [
            p[2:] for p in libs.split()   if p.startswith("-l")
        ]
        extra_compile_args = [p for p in cflags.split() if not p.startswith("-I")]
        extra_link_args    = [p for p in libs.split()   if not p.startswith(("-L", "-l"))]

    # Always include the GDAL Python bindings source shipped with GDAL itself.
    # cibuildwheel will have installed them via the system package, so we just
    # wrap the existing shared library into a Python extension.
    return Extension(
        name="osgeo._gdal",
        sources=[],           # no extra C sources; we link the system GDAL
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )


# Read version from environment (set by CI) or fall back to GDAL itself
gdal_version = os.environ.get("GDAL_VERSION", "3.9.3")

setup(
    name="gdal-wheels",
    version=gdal_version,
    description="GDAL Python bindings",
    long_description=(Path(__file__).parent / "README.md").read_text(encoding="utf-8")
    if (Path(__file__).parent / "README.md").exists()
    else "",
    long_description_content_type="text/markdown",
    author="GDAL Contributors",
    url="https://gdal.org",
    packages=["osgeo"],
    package_dir={"osgeo": "gdal_wheels/osgeo"},
    python_requires=">=3.9",
    install_requires=["numpy>=1.24"],
)
