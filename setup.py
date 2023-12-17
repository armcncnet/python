import os
import shutil
from setuptools import setup, find_packages

dist_directory = "dist"
if os.path.exists(dist_directory):
    shutil.rmtree(dist_directory)
    shutil.rmtree("build")
    shutil.rmtree("armcnc.egg-info")

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="armcnc",
    version="1.1.24",
    author="MakerYang",
    author_email="admin@wileho.com",
    description="Python development framework for armcnc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/armcnc/python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7.5",
)
