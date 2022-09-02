import glob
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCIOT",
    version="0.7.0",
    author="cclljj",
    author_email="cclljj@iis.sinica.edu.tw",
    description="Simple python module for retrieving data from Civil IOT Taiwan Data Service Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files=glob.glob("pyCIOT/config/**"),
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
    ],
    python_requires=">=3.6",
    py_modules=["pyCIOT"],
    # package_dir={"pyCIOT": "pyCIOT"},
    install_requires=["requests==2.28.0", "xmltodict==0.13.0"],
    tests_require=["pytest"],
)
