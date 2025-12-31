"""Setup configuration for PyVarChart."""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='pyvarchart',
    version='0.2.0',
    author='PyVarChart Contributors',
    author_email='',
    description='A Python library for creating variability charts with hierarchical grouping',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/Guy-Steiff/pyvarchart',
    packages=find_packages(),
    py_modules=['pyvarchart'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='visualization, variability, chart, statistics, analysis, plotting',
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'matplotlib>=3.3.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Guy-Steiff/pyvarchart/issues',
        'Source': 'https://github.com/Guy-Steiff/pyvarchart',
    },
)

