### Introduction

This is a tiny library that combines [PyFilesystem2](https://docs.pyfilesystem.org/en/latest/index.html) and [python-magic](https://pypi.org/project/python-magic/). It is built exclusively for a project I'm working on to analyse data packages that look like a bunch of files, zip/rar archives, exotic structures such as a zip file within another zip, etc.

Could it be useful for other puroposes? maybe, if you want to [use pyfilesystem2](https://docs.pyfilesystem.org/en/latest/guide.html#why-use-pyfilesystem) with
 - [rar archives](https://rarfile.readthedocs.io/index.html)
 - and to apply a little [magic](https://pypi.org/project/python-magic/) to find out a signal within a messy data pile :-)


### Installation

#### Native dependencies
macOS:
```
brew install libmagic rar
```

Docker(Ubuntu):
```
TODO
```

#### This library 
```
pip install git+https://github.com/vitaly-d/magic_fs
```

### Usage:
```python

from magic_fs.fs import OSFS, mount_archive

def walk(fs):
    for path in fs.walk.files():
        archive_fs = mount_archive(fs, path)
        if archive_fs is not None:
            archive_fs.tree()
            walk(archive_fs)

        # do something useful for given path
        print(path, fs.magic(path))

```


### Development hints
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements
python -m pep517.build .
```


