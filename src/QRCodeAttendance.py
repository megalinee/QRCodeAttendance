import tkinter as tk
import pandas as pd
import json
import qrcode
import cv2
import io
import threading
from datetime import date
from tkinter import ttk, Listbox, Frame, ANCHOR, Button, Label, END
from os.path import exists


pathToJSON = "./data.json"

GENERAL_DATE = "Friday"

primary_color = "#ff5e5e"
secondary_color = "black"

if not exists(pathToJSON):
    f = open(pathToJSON, "a")
    f.write("{\"members\":[],\"member-count\": 0}")
    f.close()


def read_json(filename=pathToJSON):
    with open(filename,) as file:
        return json.load(file)


def write_json(new_data, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["members"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def increment_user_count(inc, filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["member-count"] = file_data["member-count"]+inc
        file.seek(0)
        json.dump(file_data, file, indent=4)


def text_QR_code(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()


def parse_nested_json(json_d):
    result = {}
    for key in json_d.keys():
        if not isinstance(json_d[key], dict):
            result[key] = json_d[key]
        else:
            result.update(parse_nested_json(json_d[key]))
    return result


def json_to_csv(json):
    json_data = pd.read_json(json)
    json_list = [j[1][0] for j in json_data.iterrows()]
    parsed_list = [parse_nested_json(j) for j in json_list]
    result = pd.DataFrame(parsed_list)
    result.to_csv("data.csv", index=False)


# Window Generation
root = tk.Tk()
root.title('Admin Dashboard')
root.geometry("598x300")
root.resizable(False, False)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Manage Members')
tabControl.add(tab2, text='Add Members')
tabControl.add(tab3, text='Other')
tabControl.pack(expand=1, fill="both")

# -------------------------------------------
#  Manage Members Tab
#
#  Tab used to manage members
# -------------------------------------------
center = Frame(tab1, bg='gray2', width=100, height=200)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

center.grid(row=0, sticky="nsew")

ctr_left = Frame(center, bg=primary_color, width=100, height=190, padx=5)
ctr_mid = Frame(center, bg=secondary_color, width=100, height=190, padx=5)
ctr_right = Frame(center, bg=secondary_color, width=100, height=190, padx=5)
ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="ns")
ctr_right.grid(row=0, column=2, sticky="ns")

member_list = Listbox(ctr_left)
member_list.pack(pady=15, padx=1)

qr_display = tk.Text(ctr_right, height=15, width=30)
qr_display.configure(state='disable')
qr_display.pack(pady=15, padx=(5, 10))

info_display = tk.Text(ctr_mid, height=15, width=20)
info_display.pack(pady=15, padx=(10, 5))
info_display.insert(tk.END, "ID:\nDays Attended:")
info_display.configure(state='disable')


def reload_member_list():
    file_data = read_json()
    member_list.delete(0, END)
    for i in range(len(file_data["members"])):
        member_list.insert(i, file_data["members"][i]["name"])


reload_member_list()


def select_user():
    file_data = read_json()
    for i in range(len(file_data["members"])):
        if file_data["members"][i]["name"] == member_list.get(ANCHOR):
            user = file_data["members"][i]
            info_display.configure(state='normal')
            info_display.delete('1.0', END)
            qr_display.configure(state='normal')
            qr_display.delete('1.0', END)

            # Display ID
            info_display.insert(tk.END, "ID:\n" +
                                str(user["id"]))

            # Display QR code
            qr_display.insert(tk.END, text_QR_code(user["id"]))

            # Display Days attended
            info_display.insert(tk.END, "\nDays Attended:")
            for day in user["days-attended"]:
                if user["days-attended"][day] == True:
                    info_display.insert(tk.END, "\n" + day)

            info_display.configure(state='disable')
            qr_display.configure(state='disable')
            break


def remove_user(filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["name"] == member_list.get(ANCHOR):
                del file_data["members"][i]
                file_data["member-count"] -= 1
                break
        file.seek(0)
        updatedJSON = json.dumps(file_data, indent=4)
    with open(filename, 'w') as file:
        file.write(updatedJSON)
        file.close()
    member_list.delete(ANCHOR)


select_button = Button(ctr_left, text='Select', command=select_user)
select_button.pack(pady=5)

delete_button = Button(ctr_left, text='Delete', command=remove_user)
delete_button.pack(pady=5)

# -------------------------------------------
#  Add Members Tab
#
#  Tab used to add members
# -------------------------------------------
full_name_var = tk.StringVar()
graduating_year_var = tk.StringVar()

center = Frame(tab2, bg='black', width=100, height=200)

center.grid(row=0, sticky="nsew")

ctr_left = Frame(center, bg=primary_color, width=100, height=190, padx=5)
ctr_mid = Frame(center, bg=secondary_color, width=100, height=190, padx=5)
ctr_right = Frame(center, bg=secondary_color, width=100, height=190, padx=5)
ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="ns")
ctr_right.grid(row=0, column=2, sticky="ns")


name_label = Label(ctr_left, text="Full Name")
name_label.pack(pady=(20, 5))

name_entry = ttk.Entry(ctr_left, textvariable=full_name_var)
name_entry.pack()
name_entry.focus()


year_label = Label(ctr_left, text="Graduating Year\n(ex. 2023)")
year_label.pack(pady=(20, 5))

year_entry = ttk.Entry(ctr_left, textvariable=graduating_year_var)
year_entry.pack()
year_entry.focus()


add_qr_display = tk.Text(ctr_right, height=15, width=30)
add_qr_display.configure(state='disable')
add_qr_display.pack(pady=15, padx=(5, 10))

add_info_display = tk.Text(ctr_mid, height=15, width=20)
add_info_display.pack(pady=15, padx=(10, 5))
add_info_display.insert(tk.END, "")
add_info_display.configure(state='disable')


def submit_user():
    full_name = str(full_name_var.get())
    graduating_year = str(graduating_year_var.get())
    file_data = read_json()
    if len(graduating_year) > 2:
        graduating_year = graduating_year[-2:]

    avalID = "00"
    if len(file_data["members"]) > 0:
        lastMemberID = str(
            file_data["members"][len(file_data["members"])-1]["id"])[-2:]
        avalID = str((int(lastMemberID) + 1)).zfill(2)
    idnum = int(graduating_year + avalID)
    write_json({"id": idnum,
                "name": full_name,
                "days-attended": {

                }}
               )
    increment_user_count(1)

    add_info_display.configure(state='normal')
    add_info_display.delete('1.0', END)
    add_qr_display.configure(state='normal')
    add_qr_display.delete('1.0', END)

    add_info_display.insert(tk.END, "Successfully added!\nName:\n" + full_name +
                            "\nID:\n" + str(idnum))
    add_qr_display.insert(tk.END, text_QR_code(idnum))

    add_info_display.configure(state='disable')
    add_qr_display.configure(state='disable')

    reload_member_list()


submit_button = Button(ctr_left, text='Submit', command=submit_user)
submit_button.pack(pady=20)

# -------------------------------------------
#  Others tab
#
#  Tab for michellanous functions
# -------------------------------------------

#  QR Code Camera

# Font Settings
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20, 30)
fontScale = 1
fontColor = (255, 255, 255)
thickness = 3
lineType = 2

# Last Detected Counter
global lastDetected
lastDetected = 0

qrDecoder = cv2.QRCodeDetector()

# Date Getter
dateToday = date.today()
dateString = dateToday.strftime("%m-%d-%Y")


def add_date(filename=pathToJSON):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        if len(file_data["members"]) > 0 and dateString not in file_data["members"][0]["days-attended"]:
            for member in file_data["members"]:
                member["days-attended"][dateString] = False
            file.seek(0)
            json.dump(file_data, file, indent=4)


def change_user_attendance(idnum, filename=pathToJSON):
    name = None
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for member in file_data["members"]:
            if member["id"] == idnum:
                name = member["name"]
                member["days-attended"][dateString] = True
        file.seek(0)
        updatedJSON = json.dumps(file_data, indent=4)
    with open(filename, 'w') as file:
        file.write(updatedJSON)
        file.close()
    return name


def start_camera():
    add_date()
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        global lastDetected
        lastDetected += 1

        ret, frame = vid.read()

        msg = ""
        data, points, _ = qrDecoder.detectAndDecode(frame)
        if data and lastDetected > 50:
            lastDetected = 0
            value = int(data)
            user = change_user_attendance(value)
            if user is not None:
                msg = "Welcome " + user + "!"
            else:
                msg = "Invalid User ID: " + str(value)
            recognizedFrame = frame.copy()
            cv2.putText(recognizedFrame, msg, bottomLeftCornerOfText,
                        font, fontScale, fontColor, thickness, lineType)
            cv2.imshow('poop', recognizedFrame)
        cv2.imshow('Live Feed', frame)
        if cv2.waitKey(1) == ord('q'):
            break

        if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
            break
    vid.release()
    cv2.destroyAllWindows()


def start_camera_thread():
    camera_thread = threading.Thread(target=start_camera)
    camera_thread.start()


start_camera_button = Button(
    tab3, text='Start QR Scanner', command=start_camera_thread)
start_camera_button.pack(pady=5)


def export_csv():
    json_to_csv("data.json")
    export_csv_label.config(text="Generated file in this directory!")


export_csv_button = Button(tab3, text='Export CSV', command=export_csv)
export_csv_button.pack(pady=5)
export_csv_label = Label(tab3, text="")
export_csv_label.pack()

root.mainloop()
