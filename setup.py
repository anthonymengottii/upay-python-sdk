"""
Setup do pacote upay-python
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="upay-python",
    version="1.0.0",
    author="Upay",
    author_email="suporte@upaybr.com",
    description="SDK oficial da Upay para Python - Integração fácil com a API de pagamentos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthonymengottii/upay-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    keywords="upay payment pix boleto credit-card gateway sdk python",
    project_urls={
        "Bug Reports": "https://github.com/anthonymengottii/upay-python-sdk/issues",
        "Source": "https://github.com/anthonymengottii/upay-python-sdk",
        "Documentation": "https://docs.upaybr.com",
    },
)
