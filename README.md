### Introduction

This is a tiny library that combines [PyFilesystem2](https://docs.pyfilesystem.org/en/latest/index.html) and [python-magic](https://pypi.org/project/python-magic/). It is built exclusively for a project I'm working on to carry analysis of data out  that looks like a bunch of files, zip/rar archives, exotic structures sich as a zip file within another zip, etc.

Could it be useful for other puroposes? Probably yes, if you want to [use pyfilesystem2](https://docs.pyfilesystem.org/en/latest/guide.html#why-use-pyfilesystem) with
 - [rar archives](https://rarfile.readthedocs.io/index.html)
 - and to apply a little [magic](https://pypi.org/project/python-magic/) to find out a signal within a messy data pile :-)


### Installation

#### Native libraries
```
macOS:
brew install libmagic rar

Ubuntu:
```

#### Python 
```pip install .
```


### Development hints
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements
python -m pep517.build .
```


