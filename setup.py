import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taginfo",
    version="0.0.5",
    author="Mateusz Konieczny",
    description="A small wrapper around taginfo API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/taginfo_api_wrapper_in_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    install_requires=["osm_bot_abstraction_layer"], # strictly speaking only running tests requires it...
    # for dependencies see https://python-packaging.readthedocs.io/en/latest/dependencies.html
) 


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
