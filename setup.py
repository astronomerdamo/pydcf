import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydcf",
    version="1.0.0",
    author="Damien Robertson",
    author_email="robertsondamien@gmail.com",
    description="A Python cross correlation tool for unevenly sampled time series.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astronomerdamo/pydcf",
    packages=[
        'pydcf',
    ],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
    ],
)
