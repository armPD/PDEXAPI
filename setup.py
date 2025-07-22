from setuptools import setup, find_packages
# install package with:
# uv pip install -e path/to/the/projetc

setup(
    name="pdexapi",
    version="0.1.0",
    packages=find_packages(include=["pdexapi", "pdexapi.*"]),  
)