import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QSizePolicy, QInputDialog, QFileDialog, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
import subprocess
from zeroconf import ServiceBrowser, Zeroconf
import qrcode
import time

# QR Code Generator variables
TYPE = "_adb-tls-pairing._tcp.local."
NAME = "debug"
PASS = "123456"
FORMAT_QR = "WIFI:T:ADB;S:%s;P:%s;;"
CMD_PAIR = "adb pair %s:%s %s"
PAIRING = False

# QR Code Generator Class
class QRListener:
    def remove_service(self, zeroconf, type, name):
        global PAIRING
        print("Service %s removed." % name)
        print("Press enter to exit...\n")
        PAIRING = False

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added." % name)
        print("service info: %s\n" % info)
        self.pair(info)

    def pair(self, info):
        cmd = CMD_PAIR % (info.server, info.port, PASS)
        print(cmd)
        subprocess.run(cmd, shell=True)

# MainWindow Class
class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()

        # Window Title
        self.setWindowTitle("Scrcpy Tools")

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

        button3 = QPushButton("Sound")
        button3.setIcon(QIcon("icons/sound.svg"))
        button3.setIconSize(QSize(60, 60))
        button3.pressed.connect(self.sound)
        button3.setSizePolicy(sizePolicy)
        button3.setStyleSheet(buttonStyle)
        button3.setToolTip("Play the phone's audio on this device [NEEDS PAIRING]")
        gridLayout.addWidget(button3, 1, 0)

        button4 = QPushButton("Send")
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

        # Set the stretch factor for both rows to ensure buttons scale vertically
        gridLayout.setRowStretch(0, 1)
        gridLayout.setRowStretch(1, 1)
        gridLayout.setRowStretch(2, 1)

        # Set the layout of the central widget
        centralWidget.setLayout(gridLayout)

        # Set the central widget of the Window
        self.setCentralWidget(centralWidget)
        
        # Create the menu bar
        menuBar = self.menuBar()

        # Create the "File" menu
        fileMenu = menuBar.addMenu("File")

        # Add actions to the "File" menu
        fileMenu.addAction("Pair wireless device", self.pairWireless)  # Placeholder for an openFile method
        fileMenu.addAction("Restart ADB Server", self.restartAdb)  # Placeholder for an openFile method
        fileMenu.addAction("Exit", self.close)  # Use the built-in close method to exit

        # Create the "Help" menu
        helpMenu = menuBar.addMenu("Help")

        # Add actions to the "Help" menu
        helpMenu.addAction("About", self.showAbout)  # Placeholder for a showAbout method


    def mirror_screen(self):
        print("Mirror Screen")
        os.system("scrcpy --window-title='Screen Mirror' --mouse-bind=++++")

    def otg_control(self):
        print("OTG Control")
        os.system("scrcpy --window-title='OTG Control' --otg")
    
    def sound(self):
        print("Sound")
        os.system("scrcpy --window-title='Sound' --no-video --no-control")
    
    def send(self):
        text, ok = QInputDialog.getText(self, "Send Text", "Enter text to send:")
        if ok and text:
            # Replace spaces with '%s' for ADB command compatibility
            text = text.replace(' ', '%s')
            os.system(f"adb shell input text {text}")

    def transfer_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)")
        
        if files:
            for file_path in files:
                adb_command = f"adb push '{file_path}' /sdcard/Download/"
                os.system(adb_command)
            
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
                
                os.system(f"adb shell am start -a android.intent.action.VIEW -d file:///sdcard/Download/{file_name} -t {mime_type}")
            
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
                result = os.system(adb_command)
                if result == 0:
                    QMessageBox.information(self, "Installation Successful", f"App installed: {file_path.split('/')[-1]}")
                else:
                    QMessageBox.warning(self, "Installation Failed", f"Failed to install: {file_path.split('/')[-1]}")
        else:
            print("No APK files selected.")

    def restartAdb(self):
        os.system("adb kill-server")
        os.system("adb start-server")
        QMessageBox.information(self, "ADB Server", "ADB Server restarted sucessfully")

    def showAbout(self):
        QMessageBox.about(self, "About", "Scrcpy Tools\n\nVersion: 1.0\nAuthor: JCionx\n\nA simple GUI for scrcpy tools.")

    def pairWireless(self):
        global PAIRING
        PAIRING = True
        text = FORMAT_QR % (NAME, PASS)
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("pair_qr.png")  # Display the QR code image

        zeroconf = Zeroconf()
        listener = QRListener()
        browser = ServiceBrowser(zeroconf, TYPE, listener)
    
        try:
            dialog = QDialog()
            lay = QVBoxLayout(dialog)
            label = QLabel()
            lay.addWidget(label)
            pixmap = QPixmap("pair_qr.png")
            label.setPixmap(pixmap)
            dialog.exec()
            while PAIRING:
                time.sleep(0.1)
                print(PAIRING)
        finally:
            zeroconf.close()

        ip, ok = QInputDialog.getText(self, "Pair Wireless Device", "Enter the Wireless Debugging IP and Port:")
        if ok and ip:
            os.system(f"adb connect {ip}")
            QMessageBox.information(self, "Wireless Device Pairing", f"Wireless Device paired successfully")
        else:
            QMessageBox.warning(self, "Wireless Device Pairing", "Port not provided")
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()