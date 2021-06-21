rm dist -rf
python3 setup.py sdist bdist_wheel
cd dist
pip3 uninstall example_pkg_matkoniecz -y
pip3 install --user *.whl
cd ..
python3 -m "nose"
# twine upload dist/* # to upload to PyPi
