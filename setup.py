from __future__ import absolute_import, division, print_function

import os

from setuptools import setup

import versioneer

rootpath = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


long_description = '{}\n{}'.format(read('README.rst'), read('CHANGES.txt'))
LICENSE = read('LICENSE.txt')


with open('requirements.txt') as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]

setup(
    name='odvc',
    version=versioneer.get_version(),
    license=LICENSE,
    long_description=long_description,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: BSD',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Education',
                 ],
    description='Ocean Dimensionless Vertical Coordinates',
    author='Filipe Fernandes',
    author_email='ocefpaf@gmail.com',
    maintainer='Filipe Fernandes',
    maintainer_email='ocefpaf@gmail.com',
    url='https://github.com/pyoceans/odvc',
    download_url='http://pypi.python.org/pypi/odvc',
    platforms='any',
    keywords=['CF-conventions', 'dimensionless coordinate',
              'vertical coordinate'],
    install_requires=install_requires,
    tests_require=['pytest'],
    packages=['odvc'],
    cmdclass=versioneer.get_cmdclass(),
)
