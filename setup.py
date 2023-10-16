from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ipparser',
    version='1.0.1',
    author='m8sec',
    description='Lightweight package to parse host inputs for iteration.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/m8sec/ipparser',
    license='BSD 3-clause',
    packages=find_packages(include=[
        "ipparser", "ipparser.*"
    ]),
    install_requires=['dnspython'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License"
    ]
)
