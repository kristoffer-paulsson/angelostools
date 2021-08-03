"""
The .pyx scanner helps you to scan a whole package hierarchy for Cython pyx files and
encloses them in Extensions from setuptools.
"""
import glob
from pathlib import Path

from setuptools import Extension


class PyxScanner:
    """Scans hierarchically for .pyx files in given package."""

    def __init__(self, base_path: str, glob: list = None, extra: dict = None, basic: dict = None):
        self.__base_path = str(Path(base_path))
        self.__globlist = glob if glob else ["**.pyx"]
        self.__pkgdata = extra if extra else dict()
        self.__data = basic if basic else dict()

    def scan(self) -> list:
        """Build list of Extensions to be cythonized."""
        glob_result = list()
        for pattern in self.__globlist:
            glob_path = str(Path(self.__base_path, pattern))
            glob_result += glob.glob(glob_path, recursive=True)

        extensions = list()
        for module in glob_result:
            package = ".".join(Path(module[len(self.__base_path) + 1:-4]).parts)
            data = self.__pkgdata[package] if package in self.__pkgdata else {}
            core = {"name": package, "sources": [module]}
            kwargs = {**self.__data, **data, **core}
            extensions.append(Extension(**kwargs))

        return extensions

    def list(self) -> list:
        """Build list of modules found."""
        glob_result = list()
        for pattern in self.__globlist:
            glob_path = str(Path(self.__base_path, pattern))
            glob_result += glob.glob(glob_path, recursive=True)

        modules = list()
        for module in glob_result:
            package = ".".join(Path(module[len(self.__base_path) + 1:-4]).parts)
            modules.append(package)

        return modules
