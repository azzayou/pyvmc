"""Set up the PyVMC for Installation."""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### Import Python Library
import os.path

try:
    module = __import__("distutils.core", globals(), locals()).core
except ModuleNotFoundError:
    module = __import__("setuptools", globals(), locals())

setup = module.setup


current_dir = os.path.dirname(__file__)

with open(os.path.join(current_dir, "README.md")) as file:
    long_description = file.read()


setup(
    ## About ME :D
    author="azzayou",
    author_email="azzayou9@gmail.com",
    ## Maintainers
    maintainer="azzayou",
    maintainer_email="azzayou9@gmail.com",
    ## About package
    packages=["pyvmc"],
    name="pyvmc",
    version="0.1.0",
    license="MIT",
    license_files=["LICENSE"],
    description="Python Vectors Matrices Colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azzayou/pyvmc",
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=2.7",
)
