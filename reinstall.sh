rm dist -rf
python3 setup.py sdist bdist_wheel
cd dist
pip3 uninstall taginfo -y
pip3 install --user *.whl
cd ..
python3 ../../python_package_reinstaller/reinstaller.py taginfo # yes, it relies on code on my computer - let me know if anyone else wants to run this script
python3 -m unittest
# twine upload dist/* # to upload to PyPi
