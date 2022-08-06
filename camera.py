from datetime import date
from os.path import exists
import json
import cv2

# Change this to the day of general meetings
GENERAL_DATE = "Friday"

pathToJSON = "./data.json"

dateToday = date.today()
dateString = dateToday.strftime("%m-%d-%Y")
meeting_type = "Extra"
if dateToday.strftime("%A") == GENERAL_DATE:
    meeting_type = "General"

if not exists(pathToJSON):
    f = open(pathToJSON, "a")
    f.write("{\"members\":[],\"member-count\": 0}")
    f.close()

vid = cv2.VideoCapture(0)

qrDecoder = cv2.QRCodeDetector()

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20, 30)
fontScale = 1
fontColor = (255, 255, 255)
thickness = 3
lineType = 2

lastDetected = 0


def add_date(filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        if len(file_data["members"]) > 0 and dateString + " " + meeting_type not in file_data["members"][0]["days-attended"]:
            for member in file_data["members"]:
                member["days-attended"][dateString +
                                        " " + meeting_type] = False
            file.seek(0)
            json.dump(file_data, file, indent=4)


add_date()


def change_attendance(idnum, filename=pathToJSON):
    name = None
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for member in file_data["members"]:
            if member["id"] == idnum:
                name = member["name"]
                member["days-attended"][dateString + " " + meeting_type] = True
        file.seek(0)
        updatedJSON = json.dumps(file_data, indent=4)
    with open(filename, 'w') as file:
        file.write(updatedJSON)
        file.close()
    return name


while(True):
    lastDetected += 1

    ret, frame = vid.read()

    msg = ""
    data, points, _ = qrDecoder.detectAndDecode(frame)
    if data and lastDetected > 50:
        lastDetected = 0
        value = int(data)
        user = change_attendance(value)
        if user is not None:
            msg = "Welcome " + user + "!"
        else:
            msg = "Invalid User ID: " + str(value)
        recognizedFrame = frame.copy()
        cv2.putText(recognizedFrame, msg, bottomLeftCornerOfText,
                    font, fontScale, fontColor, thickness, lineType)
        cv2.imshow('poop', recognizedFrame)

    cv2.imshow('Live Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()
