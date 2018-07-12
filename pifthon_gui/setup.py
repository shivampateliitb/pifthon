from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(

    name='pifthon',
    version='1.0',
    description='An information flow control monitor for python program',  # Required


    author='Sandip Ghosal,Arunika Yadav',
    author_git="https://github.com/sandipghosal",
    author_email='sandipsmit@gmail.com',
    project_url='https://github.com/sandipghosal/pifthon',

    license='The MIT License 2017',


    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        #'License :: IITB',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    # package=[""],
    # install_requires=[
    # 'beautifulsoup4','certifi','chardet','client','colorama','dataecorator','funcsigs',
    # 'future','idnapython','ipython-genutils','jedi','latex','mpmath','numpy','pandas',
    # 'parso','pickleshare','prompt-toolkit5','PyAudio1',
    # 'Pygments','pypiwin32ython-dateutil','pytz3','requests4','shutilwhich',
    # 'simplegeneric','six0','SpeechRecognition','sympy','tempdir','traitlets','urllib','wikipedia'
    # ],
    # package_data={},
    # data_file=[],
    # dependency_links=['']

    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/sandipghosal/pifthon/issues',
        'Possible Improvements': 'https://github.com/sandipghosal/pifthon/improvements',
    },
)
