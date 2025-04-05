import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tornet",
    version="2.1.0", 
    author="Fidal",
    author_email="youkymusasi1597@gmail.com",
    description="Automate IP address changes using Tor, compatible with Linux and Termux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hinatara/tornet-project", 
    packages=find_packages(where="."),
    package_dir={"": "."}, 
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    python_requires='>=3.7', 
    install_requires=[
        "requests[socks]>=2.20.0",
    ],
    entry_points={
        'console_scripts': [
            'tornet=tornet.cli:main', 
        ],
    },
)
