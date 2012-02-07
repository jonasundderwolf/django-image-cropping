from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "django-image-cropping",
    version = "0.4.1",
    description = "A reusable app for cropping images easily and non-destructively in Django",
    long_description=open('README.rst').read(),
    author = "jonasvp",
    author_email = "jvp@jonasundderwolf.de",
    url = "http://github.com/jonasundderwolf/django-image-cropping",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
    packages = find_packages(),
    include_package_data=True,
    install_requires = [
        'easy_thumbnails',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
