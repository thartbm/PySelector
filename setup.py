from setuptools import setup
import sys
import os

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================

Unsupported Python version
==========================
This version of Pyselect requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""")

setup(
    name='PySelector',
    version='1',
    packages=['gui', 'setting', 'database'],
    url='https://github.com/thartbm/PySelector',
    license='',
    author='Alireza Tajadod',
    author_email='ATajadod94@gmail.com',
    description='Selection Gui for Preprocessing motor-control data',
    install_requires = ['wxpython','pandas','matplotlib','numpy','scipy']
)
