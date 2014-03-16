from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("cec14_test_func",
                 sources=["_cec14_test_func.pyx", "cec14_test_func.c"],
                 include_dirs=[numpy.get_include()])],
)


