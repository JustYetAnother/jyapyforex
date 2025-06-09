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
powershell:
```bash
.venv\Scripts\Activate.ps1
```

### Install library in editable mode
```bash
python3 -m pip install -e .
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

### Upload package

TestPyPi repository

```bash
python3 -m twine upload --repository testpypi dist/*
```

PyPi repository

```bash
python3 -m twine upload dist/*
```