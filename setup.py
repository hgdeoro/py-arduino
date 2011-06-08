from distutils.core import setup

version = "0.0.1-alpha"
description = 'Communicate with Arduino from Python, a web page and JavaScript'
author="Horacio G. de Oro"
author_email = "hgdeoror@gmail.com"
url = "http://pyarduinoproxy.blogspot.com/"
package_dir = {'':'src', }
classifiers = [ # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 3 - Alpha",
    "Environment :: Console", 
    "Environment :: Web Environment", 
    "Intended Audience :: Developers", 
    "Intended Audience :: End Users/Desktop", 
    "License :: OSI Approved :: GNU General Public License (GPL)", 
    "Operating System :: OS Independent", 
    "Programming Language :: C", 
    "Programming Language :: JavaScript", 
    "Programming Language :: Python", 
    "Topic :: Communications", 
    "Topic :: Utilities",
]

setup(name='Distutils',
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    package_dir=package_dir, 
    packages=['arduino_proxy', 'arduino_proxy.ui', 'arduino_proxy.tests'],
    classifiers=classifiers, 
)

##import os
##from setuptools import setup, find_packages
##
##def read(fname):
##    return open(os.path.join(os.path.dirname(__file__), fname)).read()
##
##setup(
##    name = "PyArduinoProxy",
##    version = "0.0.1-alpha",
##    author = "Horacio G. de Oro",
##    author_email = "hgdeoror@gmail.com",
##    description = ("Communicate with Arduino from Python, "
##        "a web page and JavaScript."),
##    license = "GPL",
##    keywords = "arduino web",
##    url = "http://pyarduinoproxy.blogspot.com/",
##    package_dir = {'':'src'}, 
##    packages = find_packages('src'), 
##    classifiers=classifiers,
##)
