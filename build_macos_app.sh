sudo rm -rf build dist
python3 setup.py py2app --emulate-shell-environment --optimize 2 --strip
cd dist
create-dmg "Scrcpy Tools.app"
rm -rf "Scrcpy Tools.app"
cd ..
sudo rm -rf build
