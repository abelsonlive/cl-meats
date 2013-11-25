import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'readme.md'))
readme = f.read()
f.close()

setup(
    name='cl-meats',
    version="0.1",
    description="Command line client for chat.meatspac.es.",
    long_description=readme,
    author='Brian Abelson',
    author_email='brianabelson@gmail.com',
    url='http://github.com/abelsonlive/cl-meats/tree/master',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], 
    entry_points = {
          'console_scripts': [
                'meats = cl_meats:run', 
          ],
    },
)