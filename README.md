# QR Code Attendance
QR Code Attendance is a Python-based program that allows you to log attendance by showing a QR code to your webcam. It's logged in a generated JSON file.

# Installation
Go to this link:<br />
https://github.com/megalinee/QRCodeAttendance/archive/refs/heads/master.zip<br />
Download the zip file, unzip it, then you're ready to start using the software.

# Use
Once downloaded there will be two important files, dist/admin.exe & camera.py.<br />
admin.exe is used to enter in new members as well as get qr codes for existing members.<br />
camera.py starts up active webcam scanning for QR codes. It will read the data and automatically log if a member is present or not.

admin.exe is a simple executable file, to run it all you need to do is double click on it.

camera.py can be ran by typing "python camera.py" in command prompt while in the file's directory.<br />
Install any dependency needed be typing "pip install (dependency name)"

To retrieve the data you just need the data.json file.<br />
For use of data within Google Sheets, I reccomend the following plugin for importing the JSON file:<br />
https://workspace.google.com/marketplace/app/simple_json_import/14083189470
