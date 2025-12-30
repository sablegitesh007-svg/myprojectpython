"""
Setup configuration for the Python project.
"""

from setuptools import setup, find_packages

setup(
    name="gs-python-project",
    version="0.1.0",
    description="Python project setup",
    author="gitesh",
    author_email="sablegitesh007@gmail.com",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    python_requires=">=3.8",
)

