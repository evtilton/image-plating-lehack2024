from setuptools import setup, find_packages

setup(
    name = "yourpackage",
    version = "1.2.0",
    description = "Simple description",
    packages = find_packages(),
    install_requires = [
      'argparse',
      'time',
      'matplotlib',
      'numpy',
      'PIL',
      'scipy',
      'tqdm',
      'math',
      'datetime',
      'numba'
                       ]  # Example of external package
)
