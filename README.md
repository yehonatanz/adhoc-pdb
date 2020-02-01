# adhoc-pdb
[![Build Status](https://travis-ci.org/yehonatanz/adhoc-pdb.svg?branch=master)](https://travis-ci.org/yehonatanz/adhoc-pdb)
[![codecov](https://codecov.io/gh/yehonatanz/adhoc-pdb/branch/master/graph/badge.svg)](https://codecov.io/gh/yehonatanz/adhoc-pdb)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/adhoc-pdb.svg)](https://pypi.org/project/adhoc-pdb/)

A simple tool that allows you to debug your system whenever you want, with no overhead, even in production!

Tested on linux and OSX, should on any POSIX compliant system.

Supports `python>=2.7,>=3.5`.

### Install
`pip install adhoc-pdb` (or `pip install adhoc-pdb[cli]` to get a nice CLI)

For development, clone this repo and run `make`.

### Usage
In your code:
```python
import adhoc_pdb
adhoc_pdb.install()
```

Debug using adhoc-pdb cli:
```bash
adhoc-pdb debug <pid>
```
or using pure shell:
```bash
kill -SIGUSR1 <pid>
telnet localhost 9999
```
