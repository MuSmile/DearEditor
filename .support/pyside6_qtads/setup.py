import inspect
import os
import sys
from pathlib import Path

import cmake_build_extension
import setuptools

init_py = Path("init.py").read_text()

# Importing the bindings inside the build_extension_env context manager is necessary only
# in Windows with Python>=3.8.
# See https://github.com/diegoferigo/cmake-build-extension/issues/8.
# Note that if this manager is used in the init file, cmake-build-extension becomes an
# install_requires that must be added to the setup.cfg. Otherwise, cmake-build-extension
# could only be listed as build-system requires in pyproject.toml since it would only
# be necessary for packaging and not during runtime.
if os.name == "nt":
    init_py += "\n" + inspect.cleandoc(
        """
    import cmake_build_extension

    with cmake_build_extension.build_extension_env():
        from . import bindings
    """
    )

# Extra options passed to the CI/CD pipeline that uses cibuildwheel
CIBW_CMAKE_OPTIONS = []
if "CIBUILDWHEEL" in os.environ and os.environ["CIBUILDWHEEL"] == "1":

    if sys.platform == "linux":
        CIBW_CMAKE_OPTIONS += ["-DCMAKE_INSTALL_LIBDIR=lib"]

    if os.name == "nt":
        CIBW_CMAKE_OPTIONS += []

setuptools.setup(
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="Pyside6-QtAds",
            install_prefix="pyside6_qtads",
            write_top_level_init=init_py,
            source_dir=str(Path(__file__).parent.absolute()),
            cmake_configure_options=[
                "-DBUILD_EXAMPLES:BOOL=OFF",
                f"-DPython3_ROOT_DIR={Path(sys.prefix)}",
            ]
            + CIBW_CMAKE_OPTIONS,
        ),
    ],
    cmdclass=dict(
        build_ext=cmake_build_extension.BuildExtension,
    ),
)
