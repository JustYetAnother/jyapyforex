## How to build and upload files

### Clean existing files
rm -rf dist/*

### Build package

python3 -m build


### Upload package
python3 -m twine upload dist/*