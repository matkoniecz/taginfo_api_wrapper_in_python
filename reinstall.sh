rm dist -rf
python3 setup.py sdist bdist_wheel
cd dist
pip3 uninstall taginfo -y
pip3 install --user *.whl
python3.10 -m pip uninstall taginfo -y
python3.10 -m pip install --user *.whl
cd ..
python3 -m unittest
# twine upload dist/* # to upload to PyPi
