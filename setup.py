#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, "src", "django_mb", "__init__.py")

reqs = "install.py%d.pip" % sys.version_info[0]


def get_version(*file_paths):
    """Retrieves the version from django_mb/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = [\"]([^\"]*)[\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version(init)


def read(*files):
    content = ""
    for f in files:
        content += codecs.open(os.path.join(ROOT, "src",
                                            "requirements", f), "r").read()
    return content


tests_requires = read("testing.pip")
dev_requires = tests_requires + read("develop.pip")
install_requires = read("install.any.pip", reqs)

readme = codecs.open("README.rst").read()
history = codecs.open("CHANGES.rst").read().replace(".. :changelog:", "")

setup(
    name="django-message-broker",
    version=version,
    description="""django app to send updates/creations/deletions to message broker topic""",
    long_description=readme,
    author="Stefano Apostolico",
    author_email="s.apostolico@gmail.com",
    url="https://github.com/saxix/django-mb",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=dev_requires,
    extras_require={
        "dev": dev_requires,
        "test": tests_requires,
        "kafka": ["kafka-python==1.3.2"],
        "rabbit": ["pika"],
    },
    license="BSD",
    zip_safe=False,
    keywords="django-mb",
    package_data={
        "django_mb": [
            "locale/*/LC_MESSAGES/django.po", "locale/*/LC_MESSAGES/django.mo"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
