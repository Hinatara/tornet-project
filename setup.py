import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tornet",
    version="2.1.0", # Incremented version
    author="Fidal",
    author_email="your_email@example.com", # Optional: Add your email
    description="Automate IP address changes using Tor, compatible with Linux and Termux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/tornet", # Optional: Add repo URL
    packages=find_packages(where="."), # Find packages in the current directory
    package_dir={"": "."}, # Package root is the current directory
    include_package_data=True, # Include non-code files specified in MANIFEST.in (if any)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose an appropriate license
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    python_requires='>=3.7', # Specify minimum Python version
    install_requires=[
        "requests[socks]>=2.20.0", # Specify dependencies
    ],
    entry_points={
        'console_scripts': [
            'tornet=tornet.cli:main', # Creates the 'tornet' command
        ],
    },
)