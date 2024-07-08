![banner](https://github.com/JCionx/scrcpy-tools/assets/92257741/99f6a9ba-c935-4173-9256-15f879aee079)

## Screenshots
![Screenshot_20240708_153922](https://github.com/JCionx/scrcpy-tools/assets/92257741/23dfdb50-96a6-4b72-9083-98da9989d141)

## Compatibility
### Linux
Tested on Debian
### macOS
Tested on macOS Sequoia
### Windows
Probably won't work

## Installation
### Linux
```
# Install ADB
sudo apt install adb

# Install scrcpy
git clone https://github.com/Genymobile/scrcpy
cd scrcpy
./install_release.sh

# Run Scrcpy Tools
git clone https://github.com/JCionx/scrcpy-tools
cd scrcpy-tools
pip install -r requirements.txt
python3 main.py
```

### macOS
```
# Install ADB
brew install adb

# Install scrcpy
brew install scrcpy

# Run Scrcpy Tools
git clone https://github.com/JCionx/scrcpy-tools
cd scrcpy-tools
pip install -r requirements.txt
python3 main.py
```
