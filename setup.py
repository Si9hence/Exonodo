from setuptools import setup, find_packages

setup(
    name = "Exonodo",
    version = "0.1.0",
    packages = find_packages(),
    install_requires = ["requests",
    "requests_html"]
)

