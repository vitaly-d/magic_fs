### Introduction

This is a tiny library that combines [PyFilesystem2](https://docs.pyfilesystem.org/en/latest/index.html) and [python-magic](https://pypi.org/project/python-magic/). It is built for a project I'm working on to analyse data packages that look like a bunch of files, zip/rar archives, exotic structures such as a zip file within another zip, etc.

Could it be useful for you? Maybe, especially if you want 
 - to add a little bit of [magic](https://pypi.org/project/python-magic/) into [pyfilesystem2](https://docs.pyfilesystem.org/en/latest/guide.html#why-use-pyfilesystem) to find out a signal within a messy data pile 😄
 - to open [rar archives](https://rarfile.readthedocs.io/index.html) with [pyfilesystem2](https://docs.pyfilesystem.org/en/latest/guide.html#why-use-pyfilesystem)


### Installation

#### Native dependencies
macOS:
```
brew install unrar libmagic
```

Docker(Ubuntu):
```
RUN apt-get update && apt-get install -y unrar libmagic1
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
            continue

        # do something useful for given path
        print(path, fs.magic(path))
        
walk(OSFS("/Volumes/Dataset"))        

```


### Development hints
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements
python -m pep517.build .
```


