import os

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

IGNORED_DIRS = [
    "src/arduino_proxy/webui/static/jquery-ui/development-bundle/demos", 
    "src/arduino_proxy/webui/static/jquery-ui/development-bundle/docs", 
]

def gen_data_files():
    directory = os.path.join(os.path.split(__file__)[0], 'src', 'arduino_proxy', 'webui', 'static')
    all_files = []
    IGNORED_DIRS2 = [ item + '/' for item in IGNORED_DIRS ]
    for dirpath, dirnames, filenames in os.walk(directory):
        #print "dirpath:", dirpath
        if dirpath in IGNORED_DIRS:
            continue
        if [ item for item in IGNORED_DIRS2 if dirpath.startswith(item) ]:
            continue
        fixed_dirpath = '/'.join(dirpath.split('/')[1:])
        all_files.append([fixed_dirpath, [os.path.join(dirpath, f) for f in filenames]])
    return all_files

name = "PyArduinoProxy"
version = "0.0.1-alpha"
description = 'Communicate with Arduino from Python, a web page and JavaScript'
author="Horacio G. de Oro"
author_email = "hgdeoror@gmail.com"
url = "http://pyarduinoproxy.blogspot.com/"
packages = ['arduino_proxy', 'arduino_proxy.ui', 'arduino_proxy.tests', 'arduino_proxy.webui']
package_dir = {'arduino_proxy':'src/arduino_proxy', }
requires = [
    'cherrypy (>=3.2)',
    'simplejson (>=2.1)',
    'jinja2'
]

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

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

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
    data_files=gen_data_files(), 
    requires=requires, 
)
