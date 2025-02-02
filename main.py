import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QSizePolicy, QInputDialog, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QRadioButton, QGroupBox, QCheckBox, QLineEdit
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtCore import QSize, QSettings
import subprocess

version = "1.0.1"
organization = "jcionx"
product_name = "scrcpy_tools"

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        title_style = """
        QLabel {
            font-size: 20px;
            font-weight: bold;
        }
        """

        # Layout
        layout = QVBoxLayout()

        # Mirror Screen Settings
        self.mirror_screen_title = QLabel("Mirror Screen")
        self.mirror_screen_title.setStyleSheet(title_style)
        self.otg_mirror_checkbox = QCheckBox("Enable OTG Control while mirroring screen (does not work on Windows)")
        
        layout.addWidget(self.mirror_screen_title)
        layout.addWidget(self.otg_mirror_checkbox)

        # Audio Mode Settings
        self.audio_mode_title = QLabel("Audio Mode")
        self.audio_mode_title.setStyleSheet(title_style)
        self.audio_mode_buffer_label = QLabel("Audio Buffer (ms):")
        self.audio_mode_buffer = QLineEdit()
        # make it only accept int numbers
        self.audio_mode_buffer.setValidator(QIntValidator())
        layout.addWidget(self.audio_mode_title)
        layout.addWidget(self.audio_mode_buffer_label)
        layout.addWidget(self.audio_mode_buffer)

        # Save button
        self.saveButton = QPushButton("Save")
        layout.addWidget(self.saveButton)
        
        # Set dialog layout
        self.setLayout(layout)
        
        # Connect signals to slots
        self.saveButton.clicked.connect(self.save_settings)

        # Load settings at initialization
        self.load_settings()    

    def save_settings(self):
        settings = QSettings(organization, product_name)
        settings.setValue('otg_mirror_enabled', self.otg_mirror_checkbox.isChecked())
        settings.setValue('audio_buffer', self.audio_mode_buffer.text())
        self.accept()

    def load_settings(self):
        settings = QSettings(organization, product_name)
        otg_mirror_enabled = settings.value('otg_mirror_enabled', defaultValue=False, type=bool)
        audio_buffer = settings.value('audio_buffer', defaultValue="200", type=str)
        self.otg_mirror_checkbox.setChecked(otg_mirror_enabled)
        self.audio_mode_buffer.setText(audio_buffer)

# MainWindow Class
class MainWindow(QMainWindow):      
    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("Scrcpy Tools")

        self.setWindowIcon(QIcon("icons/logo_small.png"))

        self.setMinimumSize(600, 400)

        settings = QSettings(organization, product_name)

        # Create a central widget and a grid layout
        centralWidget = QWidget()
        gridLayout = QGridLayout()

        # Set size policy for buttons to expand both vertically and horizontally
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Set button style
        buttonStyle = """
        QPushButton {
            padding: 20px;
            font-size: 20px;
        }
        """

        button1 = QPushButton("Mirror Screen")
        button1.setIcon(QIcon("icons/mirror.svg")) 
        button1.setIconSize(QSize(60, 60))
        button1.pressed.connect(self.mirror_screen)
        button1.setSizePolicy(sizePolicy)
        button1.setStyleSheet(buttonStyle)
        button1.setToolTip("Mirror and control the phone's screen using Scrcpy [NEEDS PAIRING]")
        gridLayout.addWidget(button1, 0, 0)

        button2 = QPushButton("OTG Control")
        button2.setIcon(QIcon("icons/control.svg"))
        button2.setIconSize(QSize(60, 60))
        button2.pressed.connect(self.otg_control)
        button2.setSizePolicy(sizePolicy)
        button2.setStyleSheet(buttonStyle)
        button2.setToolTip("Send mouse and keyboard input directly to the phone [NEEDS USB CONNECTION]")
        gridLayout.addWidget(button2, 0, 1)

        button3 = QPushButton("Audio Mode")
        button3.setIcon(QIcon("icons/sound.svg"))
        button3.setIconSize(QSize(60, 60))
        button3.pressed.connect(self.sound)
        button3.setSizePolicy(sizePolicy)
        button3.setStyleSheet(buttonStyle)
        button3.setToolTip("Play the phone's audio on this device [NEEDS PAIRING]")
        gridLayout.addWidget(button3, 1, 0)

        button4 = QPushButton("Send text")
        button4.setIcon(QIcon("icons/send.svg"))
        button4.setIconSize(QSize(60, 60))
        button4.pressed.connect(self.send)
        button4.setSizePolicy(sizePolicy)
        button4.setStyleSheet(buttonStyle)
        button4.setToolTip("Type a string of text on the device [NEEDS PAIRING]")
        gridLayout.addWidget(button4, 1, 1)

        button5 = QPushButton("Transfer File")
        button5.setIcon(QIcon("icons/file.svg"))
        button5.setIconSize(QSize(60, 60))
        button5.pressed.connect(self.transfer_file)
        button5.setSizePolicy(sizePolicy)
        button5.setStyleSheet(buttonStyle)
        button5.setToolTip("Send files to the phone [NEEDS PAIRING]")
        gridLayout.addWidget(button5, 2, 0)

        button6 = QPushButton("Install APK")
        button6.setIcon(QIcon("icons/install.svg"))
        button6.setIconSize(QSize(60, 60))
        button6.pressed.connect(self.install_apk)
        button6.setSizePolicy(sizePolicy)
        button6.setStyleSheet(buttonStyle)
        button6.setToolTip("Install Android packages on the phone [NEEDS PAIRING]")
        gridLayout.addWidget(button6, 2, 1)

        button7 = QPushButton("Open URL")
        button7.setIcon(QIcon("icons/url.svg"))
        button7.setIconSize(QSize(60, 60))
        button7.pressed.connect(self.open_url)
        button7.setSizePolicy(sizePolicy)
        button7.setStyleSheet(buttonStyle)
        button7.setToolTip("Open URL on the phone [NEEDS PAIRING]")
        gridLayout.addWidget(button7, 3, 0)

        button8 = QPushButton("Webcam")
        button8.setIcon(QIcon("icons/webcam.svg"))
        button8.setIconSize(QSize(60, 60))
        button8.pressed.connect(self.webcam)
        button8.setSizePolicy(sizePolicy)
        button8.setStyleSheet(buttonStyle)
        button8.setToolTip("Use phone's camera as a webcam [NEEDS PAIRING]")
        gridLayout.addWidget(button8, 3, 1)

        # Set the stretch factor for both rows to ensure buttons scale vertically
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(1, 1)
        gridLayout.setRowStretch(2, 1)
        gridLayout.setRowStretch(3, 1)

        # Set the layout of the central widget
        centralWidget.setLayout(gridLayout)

        # Set the central widget of the Window
        self.setCentralWidget(centralWidget)

        # Create the menu bar
        menuBar = self.menuBar()

        # Create the "File" menu
        fileMenu = menuBar.addMenu("File")

        # Add actions to the "File" menu
        fileMenu.addAction("Pair wireless device", self.pairWireless)
        fileMenu.addAction("Restart ADB Server", self.restartAdb)
        fileMenu.addAction("Settings", self.open_settings_dialog)
        fileMenu.addAction("Exit", self.close)

        # Create the "Help" menu
        helpMenu = menuBar.addMenu("Help")

        # Add actions to the "Help" menu
        helpMenu.addAction("About", self.showAbout)  # Placeholder for a showAbout method

    def open_settings_dialog(self):
        dialog = SettingsDialog()
        dialog.exec()

    def mirror_screen(self):
        # Load settings
        settings = QSettings(organization, product_name)
        otg_mirror_enabled = settings.value('otg_mirror_enabled', defaultValue=False, type=bool)

        if otg_mirror_enabled:
            print("-M -K")
            subprocess.run("SCRCPY_ICON_PATH=\"icons/logo.svg\" scrcpy --window-title='Screen Mirror' --mouse-bind=++++ -M -K", shell=True)
        else:
            subprocess.run("SCRCPY_ICON_PATH=\"icons/logo.svg\" scrcpy --window-title='Screen Mirror' --mouse-bind=++++", shell=True)

    def otg_control(self):
        subprocess.run("SCRCPY_ICON_PATH=\"icons/logo.svg\" scrcpy --window-title='OTG Control' --otg", shell=True)
    
    def sound(self):
        settings = QSettings(organization, product_name)
        audio_buffer = settings.value('audio_buffer', defaultValue="200", type=str)
        print(audio_buffer)
        subprocess.run(f"SCRCPY_ICON_PATH=\"icons/logo_large.png\" scrcpy --window-title='Sound' --no-video --no-control --audio-buffer={audio_buffer}", shell=True)
    
    def send(self):
        text, ok = QInputDialog.getText(self, "Send Text", "Enter text to send:")
        if ok and text:
            # Replace spaces with '%s' for ADB command compatibility
            text = text.replace(' ', '%s')
            text = text.replace('&', '\\&')
            text = text.replace('*', '\\*')
            subprocess.run(f"adb shell input text \"{text}\"", shell=True)

    def transfer_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        
        if files:
            for file_path in files:
                adb_command = f"adb push '{file_path}' /sdcard/Download/"
                subprocess.run(adb_command, shell=True)
            
            if len(files) == 1:
                file_name = files[0].split('/')[-1]  # Extract the file name
                extension = file_name.split('.')[-1].lower()  # Extract the extension
                mime_type = "application/octet-stream"  # Default MIME type
                if extension in ["jpg", "jpeg", "png", "gif", "bmp"]:
                    mime_type = "image/*"
                elif extension == "mp4":
                    mime_type = "video/*"
                elif extension == "apk":
                    mime_type = "application/vnd.android.package-archive"
                elif extension == "pdf":
                    mime_type = "application/pdf"
                elif extension == "txt":
                    mime_type = "text/plain"
                elif extension == "html":
                    mime_type = "text/html"
                elif extension == "zip":
                    mime_type = "application/zip"
                
                subprocess.run(f"adb shell am start -a android.intent.action.VIEW -d file:///sdcard/Download/{file_name} -t {mime_type}", shell=True)
            
            print(f"Transferred {len(files)} files to the phone's download folder.")
            QMessageBox.information(self, "File Transfer Successful", f"Transferred {len(files)} {'files' if len(files) > 1 else 'file'} to: /sdcard/Download/")
        else:
            print("No files selected.")
            QMessageBox.warning(self, "File Transfer Failed", "No files selected.")
    
    def install_apk(self):
        # Open a file dialog to let the user select APK files
        files, _ = QFileDialog.getOpenFileNames(self, "Select APK Files", "", "APK Files (*.apk)")
        
        # Check if any files were selected
        if files:
            for file_path in files:
                # Construct the adb command to install each APK
                adb_command = f"adb install '{file_path}'"
                # Execute the adb command
                result = subprocess.run(adb_command, shell=True).returncode
                if result == 0:
                    QMessageBox.information(self, "Installation Successful", f"App installed: {file_path.split('/')[-1]}")
                else:
                    QMessageBox.warning(self, "Installation Failed", f"Failed to install: {file_path.split('/')[-1]}")
        else:
            print("No APK files selected.")

    def restartAdb(self):
        subprocess.run("adb kill-server", shell=True)
        subprocess.run("adb start-server", shell=True)
        QMessageBox.information(self, "ADB Server", "ADB Server restarted sucessfully")

    def showAbout(self):
        QMessageBox.about(self, "About", f"Scrcpy Tools\n\nVersion: {version}\nAuthor: JCionx\n\nA simple GUI for scrcpy.")

    def pairWireless(self):
        ip, ok = QInputDialog.getText(self, "Pair Wireless Device", "Enter the Pairing IP and Port:")
        if ok and ip:
            code, ok = QInputDialog.getText(self, "Pair Wireless Device", "Enter the Pairing Code:")
            if ok and ip:
                subprocess.run(f"adb pair {ip} {code}", shell=True)
                port, ok = QInputDialog.getText(self, "Pair Wireless Device", "Enter the Wireless Debugging Port:")
                if ok and ip:
                    print(f"adb connect {ip.split(":")[0]}:{port}")
                    subprocess.run(f"adb connect {ip.split(":")[0]}:{port}", shell=True)
                    QMessageBox.information(self, "Wireless Device Pairing", f"Wireless Device paired successfully")
                else:
                    QMessageBox.warning(self, "Wireless Device Pairing", "Port not provided")
            else:
                QMessageBox.warning(self, "Wireless Device Pairing", "Code not provided")
        else:
            QMessageBox.warning(self, "Wireless Device Pairing", "IP not provided")
    
    def open_url(self):
        url, ok = QInputDialog.getText(self, "Open URL", "Enter URL to open:")
        if ok and url:
            # open url with adb
            url = url.replace('&', '\\&')
            url = url.replace('*', '\\*')
            subprocess.run(f"adb shell am start -a android.intent.action.VIEW -d \"{url}\"", shell=True)

    def webcam(self):
        subprocess.run("SCRCPY_ICON_PATH=\"icons/logo.svg\" scrcpy --window-title='Webcam' --video-source=camera --no-audio --camera-size=1920x1080", shell=True)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()