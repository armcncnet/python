from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="armcnc",
    version="1.0.0",
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
