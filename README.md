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

Install ADB
```
sudo apt install adb
```

Install scrcpy
```
git clone https://github.com/Genymobile/scrcpy
cd scrcpy
./install_release.sh
```

Run Scrcpy Tools
```
git clone https://github.com/JCionx/scrcpy-tools
cd scrcpy-tools
pip install -r requirements.txt
python3 main.py
```

### macOS

Install ADB
```
brew install adb
```

Install scrcpy
```
brew install scrcpy
```

Download the dmg from the [releases](https://github.com/JCionx/scrcpy-tools/releases)

## How to connect to an Android phone
1. Enable `Developer Mode` on your phone
2. Enable `USB Debugging` in `Developer Options`
3. Connect your Android phone with a cable to your computer
4. Run Scrcpy Tools and choose any action
5. On your Android Phone check `Always Trust from this computer` then click `Trust`

## How to connect to an Android phone wirelessly
1. Disconnect all devices from Scrcpy Tools by clicking on `File > Restart ADB Server`
2. Go to `File > Pair wireless device`
3. Enable `Developer Mode` on your phone
4. Enable and open `Wireless debugging` in `Developer Options`
5. Click `Pair device with pairing code`
6. Type the text under `IP address & Port` on Scrcpy Tools
   ![share_778527781881591369](https://github.com/JCionx/scrcpy-tools/assets/92257741/73602402-8a2a-461c-b89b-ba157010f4bd)
7. Type the pairing code on Scrcpy Tools
   ![share_8014949211153857143](https://github.com/JCionx/scrcpy-tools/assets/92257741/8c9889e1-b1eb-4767-aae5-5d33a39f7962)
8. Type the Wireless debugging port on Scrcpy Tools
   ![share_975986217332931125](https://github.com/JCionx/scrcpy-tools/assets/92257741/aaf11d35-588c-48b4-ae85-b17e721d5a1f)

