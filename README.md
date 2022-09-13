# QR Code Attendance
QR Code Attendance is a Python-based program that utilizes QR codes and a live webcam scanner to log member's attendance. It offers an intuitive UI for managing members and has various methods of exporting the generated data.

# Installation
Download the latest release from this link: <br />
https://github.com/megalinee/QRCodeAttendance/releases

# Use
After installing there will be 3 different tabs.<br />
Manage Members is used to look up member's information<br />
Add Members is used to add new members<br />
Other is used to start up the camera scanner and used to export a csv file.

When the camera is shown the user's QR code it automatically logs them for that day.

Everything is saved in a data.json file found in your app data folder.

# Compiling
Within the src folder there will be a file titled `requirments.txt`.<br />
This lists all required python depencies, to install them on your local machine use the following command:<br />
`pip install -r ./src/requirements.txt`<br />

I use pyinstaller to make the file into a executable.<br />
To use it simple run the following command:<br />
`pyinstaller ./src/Main.spec`<br />

I then use Inno Setup to make it into an easy to install installer.<br />

It's highly reccomended to run this within a virtual enviornment as it uses specific and sometimes outdated versions of various python dependencies.<br />
