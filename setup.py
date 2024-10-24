import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taginfo",
    version="0.0.4",
    author="Mateusz Konieczny",
    description="A small wrapper around taginfo API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/taginfo_api_wrapper_in_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # for dependencies see https://python-packaging.readthedocs.io/en/latest/dependencies.html
) 


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
