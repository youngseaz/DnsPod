#!/usr/bin/python3

from setuptools import setup

setup(
    name="DnsPod",
    version="1.0.0",
    description="ddns powerby DnsPod",
    author="youngseaz",
    author_email="email@youngseaz.com",
    url="https://github.com/youngseaz/dnspod.git",
    install_requires=["pycryptodome",
                      "requests"
                      ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ]
)