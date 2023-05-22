import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

using_setuptools = True

setup_args = {
    "name": "angeltools",
    "version": "0.3.1",
    "url": "https://github.com/ga1008/angeltools",
    "description": "personal python small tools collection",
    "long_description": long_description,
    "author": "Guardian",
    "author_email": "zhling2012@live.com",
    "maintainer": "Guardian",
    "maintainer_email": "zhling2012@live.com",
    "long_description_content_type": "text/markdown",
    "LICENSE": "MIT",
    "packages": setuptools.find_packages(),
    "include_package_data": True,
    "zip_safe": False,
    "entry_points": {"console_scripts": [
        'txt2char = angeltools.commands:txt2chars',
        'img2char = angeltools.commands:img2chars',
        'sortbypy = angeltools.commands:text_sorted_by_first_pinyin',
    ]},
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    "install_requires": [
        "setuptools",
        "tqdm",
        "numpy",
        "psutil",
        "redis",
        "scrapy",
        "requests",
        "pygame",
        "pillow",
        "pypinyin",
        "basecolors==0.0.2",
    ],
}

setup(**setup_args)
