from setuptools import find_packages, setup

VERSION = "0.0.1"
DESCRIPTION = "A library for serializing and deserializing DHCP packets"
LONG_DESCRIPTION = (
    "A package that makes it easier to work with DHCP packets by representing them as "
    "immutable, schematized Python objects."
)

setup(
    name="dhcp-packer",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Kevin Wang",
    author_email="kaybinwang@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "typing_extensions",
    ],
    keywords="dhcp",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
