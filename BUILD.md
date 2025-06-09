# How to build and upload files

## Create virtual environment if not present
```bash
python3 -m venv .venv
```

### Activate virtual environment
On Unix-like systems (Linux, macOS)
```bash
source .venv/bin/activate
```

On Windows
```bash
.venv\Scripts\activate.bat
```
Powershell:
```bash
.venv\Scripts\Activate.ps1
```

### Install library in editable mode
```bash
python3 -m pip install -e .
```

### Test local install of library
```bash
cd test
python3 test_converters.py
```

## Publishing the library

### Install other dependencies
```bash
python3 -m pip install build twine
```

### Clean existing files
```bash
rm -rf dist/*
```

### Build package
```bash
python3 -m build
```

### Upload package to TestPyPi and test

```bash
python3 -m twine upload --repository testpypi dist/*
pip uninstall jyapyforex
pip install --index-url https://test.pypi.org/simple/  jyapyforex
cd test
python3 test_converters.py
```

### Upload package to PyPi and test

```bash
python3 -m twine upload dist/*
pip uninstall jyapyforex
pip install jyapyforex
cd test
python3 test_converters.py
```