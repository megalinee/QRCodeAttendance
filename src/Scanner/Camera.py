from datetime import datetime
import cv2
import Constants as CONSTANT
from pyzbar.pyzbar import decode
from Tools.JSONTools import read_json, write_json
from datetime import date


class Camera:
    def __init__(self):
        self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.signins = {}

        dateToday = date.today()
        self.date_string = dateToday.strftime("%m-%d-%Y")

        self.add_date()

    def start(self):
        lastDetected = 0
        while True:
            lastDetected += 1

            ret, frame = self.vid.read()

            msg = ""

            processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            detectedBarcodes = decode(processedImage)
            if detectedBarcodes and detectedBarcodes[0].data.decode().isnumeric() and lastDetected > 50:
                barcode = detectedBarcodes[0]
                lastDetected = 0
                value = int(barcode.data)
                member = self.change_user_attendance(value)
                msg = "Invalid User ID: " + str(value)
                if member is not None:
                    msg = "Welcome " + member["Name"] + "!"
                    if len(self.signins[member["ID"]]) > 1:
                        msg = "Bye " + member["Name"] + "!"
                recognizedFrame = frame.copy()
                cv2.putText(recognizedFrame, msg, CONSTANT.bottomLeftCornerOfText,
                            CONSTANT.font, CONSTANT.fontScale, CONSTANT.fontColor, CONSTANT.thickness, CONSTANT.lineType)
                cv2.imshow('poop', recognizedFrame)
            cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break

            if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
                break
        self.log_all_attendance()
        self.vid.release()
        cv2.destroyAllWindows()

    def add_date(self):
        file_data = read_json()
        if len(file_data["members"]) > 0:
            for member in file_data["members"]:
                if self.date_string not in member["days-attended"]:
                    member["days-attended"][self.date_string] = 0
        write_json(file_data)

    def change_user_attendance(self, id_num):
        file_data = read_json()
        user = None
        for member in file_data["members"]:
            if member["ID"] == id_num:
                user = member
                if id_num in self.signins:
                    self.signins[id_num].append(datetime.now())
                else:
                    self.signins[id_num] = [datetime.now()]
        return user

    def log_all_attendance(self):
        file_data = read_json()
        for member in file_data["members"]:
            if member["ID"] in self.signins:
                lastTime = datetime.now()
                if (len(self.signins[member["ID"]]) > 1):
                    lastTime = self.signins[member["ID"]][len(
                        self.signins[member["ID"]])-1]
                duration = lastTime - self.signins[member["ID"]][0]
                duration_in_s = duration.total_seconds()
                minutes = divmod(duration_in_s, 60)[0]
                member["days-attended"][self.date_string] = minutes
        write_json(file_data)
