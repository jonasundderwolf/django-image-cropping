import re
import os
import codecs
from distutils.core import setup
from setuptools import find_packages


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts)).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name="django-image-cropping",
    version=find_version("image_cropping", "__init__.py"),
    description="A reusable app for cropping images easily and non-destructively in Django",
    long_description=open('README.rst').read(),
    author="jonasvp",
    author_email="jvp@jonasundderwolf.de",
    url="http://github.com/jonasundderwolf/django-image-cropping",
    packages=find_packages(),
    include_package_data=True,
    test_suite='example.runtests.runtests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
