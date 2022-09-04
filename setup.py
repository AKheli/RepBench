#!python
#cython: language_level=3

from distutils.core import setup
from Cython.Build import cythonize

path = "algorithms/Dimensionality_Reduction/CD/logal_sign.pyx"
setup(name="fast_init_sign_vector", ext_modules=cythonize(path,compiler_directives={'language_level' : "3"}),)