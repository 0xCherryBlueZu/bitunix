from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bitunix",
    version="0.1.1",
    author="0xCherryBlue",
    author_email="0xCherryBlue@proton.me",
    description="An open source, unofficial Python client for the BitUnix cryptocurrency exchange API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xCherryBlueZu/bitunix",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
)
