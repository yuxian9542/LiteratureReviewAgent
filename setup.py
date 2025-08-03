#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

with open("CLAUDE.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="literature-review-agent",
    version="1.0.0",
    description="AI-powered academic paper analysis and summarization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Literature Review Agent",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "litreview=main:main",
            "literature-review=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="academic research literature review AI analysis PDF",
)