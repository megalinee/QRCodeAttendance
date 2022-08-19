import cv2
import Constants as CONSTANT
from pyzbar.pyzbar import decode
from Tools.JSONTools import read_json, write_json
from datetime import date


class Camera:
    def __init__(self):
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        dateToday = date.today()
        self.date_string = dateToday.strftime("%m-%d-%Y")

        self.meeting_type = "Extra"
        if dateToday.strftime("%A") == CONSTANT.general_date:
            self.meeting_type = "General"

        self.full_date = self.date_string + " " + self.meeting_type

        self.add_date()

    def start(self):
        lastDetected = 0
        while True:
            lastDetected += 1

            ret, frame = self.vid.read()

            msg = ""
            detectedBarcodes = decode(frame)
            if detectedBarcodes and lastDetected > 50:
                barcode = detectedBarcodes[0]
                lastDetected = 0
                value = int(barcode.data)
                user = self.change_user_attendance(value)
                if user is not None:
                    msg = "Welcome " + user + "!"
                else:
                    msg = "Invalid User ID: " + str(value)
                recognizedFrame = frame.copy()
                x, y, w, h = barcode.rect.left, barcode.rect.top, \
                    barcode.rect.width, barcode.rect.height
                cv2.rectangle(recognizedFrame, (x, y),
                              (x+w, y+h), CONSTANT.primary_color, 8)
                cv2.putText(recognizedFrame, msg, CONSTANT.bottomLeftCornerOfText,
                            CONSTANT.font, CONSTANT.fontScale, CONSTANT.fontColor, CONSTANT.thickness, CONSTANT.lineType)
                cv2.imshow('poop', recognizedFrame)
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break

            if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
                break
        self.vid.release()
        cv2.destroyAllWindows()

    def add_date(self):
        file_data = read_json()

        if len(file_data["members"]) > 0:
            for member in file_data["members"]:
                if self.full_date not in member["days-attended"]:
                    member["days-attended"][self.full_date] = False
        write_json(file_data)

    def change_user_attendance(self, id_num):
        name = None
        file_data = read_json()
        for member in file_data["members"]:
            if member["id"] == id_num:
                name = member["name"]
                member["days-attended"][self.full_date] = True
        write_json(file_data)
        return name
