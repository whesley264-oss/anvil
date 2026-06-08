# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Read long description from README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anvil-cli",
    version="0.3.0",
    author="Whesley",
    author_email="whesley264@gmail.com",
    description="Transform websites into Android APKs without Android Studio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whesley264-oss/anvil",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.9",
    # Don't create console script - we use our own launcher
    entry_points={
        "console_scripts": [
            "anvil-raw=anvil_cli:main",
        ],
    },
    # Don't include package_data to avoid issues
    include_package_data=False,
    install_requires=[
        "qrcode>=7.4.0",
        "Pillow>=10.0.0",
    ],
)