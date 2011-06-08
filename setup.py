import os

from distutils.core import setup

#def static_files_list():
#    all_files = []
#    directory = os.path.join(os.path.split(__file__)[0], 'src', 'arduino_proxy', 'webui', 'static')
#    for root, dirs, files in os.walk(directory):
#        for a_file in files:
#            all_files.append(os.path.join(root, a_file))
#            #all_files.append('/'.join(os.path.join(root, a_file).split('/')[2:]))
#    return all_files

name = "PyArduinoProxy"
version = "0.0.1-alpha"
description = 'Communicate with Arduino from Python, a web page and JavaScript'
author="Horacio G. de Oro"
author_email = "hgdeoror@gmail.com"
url = "http://pyarduinoproxy.blogspot.com/"

packages = ['arduino_proxy', 'arduino_proxy.ui', 'arduino_proxy.tests', 'arduino_proxy.webui']
package_dir = {'':'src', }
package_data = {'': ['webui/static/*'], }

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

#data_files_static = static_files_list()
#assert data_files_static # print data_files_static

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    package_dir=package_dir, 
    packages=packages, 
    classifiers=classifiers, 
    #    data_files=[
    #        #('arduino_proxy', static_files_list()),
    #        ('', data_files_static),
    #    ]
    #    package_data=package_data, 
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
