"""See README.md for package documentation."""

from setuptools import setup, find_packages

from io import open
from os import path

from kivy_garden.advancedfocusbehavior import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

URL = 'https://github.com/kivy-garden/advancedfocusbehavior'

setup(
    name='kivy_garden.advancedfocusbehavior',
    version=__version__,
    description='An extension of Kivy\'s FocusBehavior for easier keyboard navigation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    author='Andrew Burke',
    author_email='atburke1985@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Kivy kivy-garden focus',

    packages=['kivy_garden.advancedfocusbehavior'],
    install_requires=[],
    extras_require={
        'dev': ['pytest>=3.6', 'wheel', 'pytest-cov', 'pycodestyle'],
        'travis': ['coveralls'],
    },
    package_data={},
    data_files=[],
    entry_points={},
    project_urls={
        'Bug Reports': URL + '/issues',
        'Source': URL,
    },
)
