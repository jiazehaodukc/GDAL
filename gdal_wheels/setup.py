from setuptools import setup, Extension
import os
import subprocess
import numpy as np

def get_gdal_config(option):
    """Run gdal-config to get build flags."""
    gdal_config = os.environ.get("GDAL_CONFIG", "gdal-config")
    try:
        return subprocess.check_output([gdal_config, option]).decode().strip()
    except Exception:
        return ""

def get_include_dirs():
    inc = get_gdal_config("--cflags")
    dirs = [p[2:] for p in inc.split() if p.startswith("-I")]
    dirs.append(np.get_include())
    return dirs

def get_library_dirs():
    libs = get_gdal_config("--libs")
    return [p[2:] for p in libs.split() if p.startswith("-L")]

def get_libraries():
    libs = get_gdal_config("--libs")
    return [p[2:] for p in libs.split() if p.startswith("-l")]

gdal_version = os.environ.get("GDAL_VERSION", "3.9.3")

setup(
    name="GDAL",
    version=gdal_version,
    description="GDAL: Geospatial Data Abstraction Library",
    author="Frank Warmerdam",
    license="MIT",
    packages=["osgeo"],
    package_dir={"osgeo": "osgeo"},
    ext_modules=[
        Extension(
            "osgeo._gdal",
            sources=["extensions/gdal_wrap.cpp"],
            include_dirs=get_include_dirs(),
            library_dirs=get_library_dirs(),
            libraries=get_libraries(),
            extra_compile_args=["-std=c++11"],
        )
    ],
    zip_safe=False,
    python_requires=">=3.9",
)
