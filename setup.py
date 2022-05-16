
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCIOT",
    version="0.0.2",
    author="cclljj",
    author_email="cclljj@iis.sinica.edu.tw",
    description="Simple python module for retrieving data from Civil IOT Taiwan Data Service Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="pyCIOT"),
    url="https://github.com/IISNRL/pyCIOT",
    project_urls={
        # "Documentation": "",
        "Source": "https://github.com/IISNRL/pyCIOT",
        "Bug Tracker": "https://github.com/IISNRL/pyCIOT/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["pyCIOT"],                  # Name of the python package
    package_dir={'':'pyCIOT'},              # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)