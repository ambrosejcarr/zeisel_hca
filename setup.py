from setuptools import setup

setup(
    name='zeisel',
    description='processing scripts for zeisel data',
    author='Ambrose J. Carr',
    author_email='mail@ambrosejcarr.com',
    package_dir={'': 'src'},
    packages=['zeisel'],
    install_requires=['seqc']
)
