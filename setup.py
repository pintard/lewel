from setuptools import setup, find_packages
from package import Package

setup(
    name='lewel',
    description='simple welcome screen and diagnostic program for shell',
    version='1.0',
    license='MIT',
    author='reshaun',
    author_email='pintardr@gmail.com',
    packages=find_packages(),
    cmdclass={
        "package": Package
    }
)
