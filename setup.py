from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "image_cropping",
    version = "0.1",
    description = "an app for cropping images",
    author = "JVP",
    author_email = "jvp@jonasundderwolf.de",
    url = "dev.jonasundderwolf.de:image_cropping.git",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found
    #recursively.)
    packages = find_packages(),
    include_package_data=True,
    install_requires = [
        'docutils',
        'PIL',
        'easy_thumbnails',
    ],
)
