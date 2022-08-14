import tkinter as tk
import Constants as CONSTANT
from Tools.QRTools import text_QR_code
from tkinter import ttk, Frame, Listbox, END, ANCHOR, Button
from Tools.JSONTools import read_json, write_json


class ManageMembersTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        center = Frame(self, bg='gray2', width=100, height=200)

        center.grid(row=0, sticky="nsew")

        self.ctr_left = Frame(
            center, bg=CONSTANT.primary_color, width=100, height=190, padx=5)
        self.ctr_mid = Frame(
            center, bg=CONSTANT.secondary_color, width=100, height=190, padx=5)
        self.ctr_right = Frame(
            center, bg=CONSTANT.secondary_color, width=100, height=190, padx=5)
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_mid.grid(row=0, column=1, sticky="ns")
        self.ctr_right.grid(row=0, column=2, sticky="ns")

        self.generate_UI_components()

    def generate_UI_components(self):
        self.member_list = Listbox(self.ctr_left)
        self.member_list.pack(pady=15, padx=1)
        self.reload_member_list()

        self.qr_display = tk.Text(self.ctr_right, height=15, width=30)
        self.qr_display.configure(state='disable')
        self.qr_display.pack(pady=15, padx=(5, 10))

        self.info_display = tk.Text(self.ctr_mid, height=15, width=20)
        self.info_display.pack(pady=15, padx=(10, 5))
        self.info_display.insert(tk.END, "ID:\nDays Attended:")
        self.info_display.configure(state='disable')

        select_button = Button(
            self.ctr_left, text='Select', command=self.select_user)
        select_button.pack(pady=5)

        delete_button = Button(
            self.ctr_left, text='Delete', command=self.remove_user)
        delete_button.pack(pady=5)

    def select_user(self):
        file_data = read_json()
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["name"] == self.member_list.get(ANCHOR):
                user = file_data["members"][i]
                self.info_display.configure(state='normal')
                self.info_display.delete('1.0', END)
                self.qr_display.configure(state='normal')
                self.qr_display.delete('1.0', END)

                # Display ID
                self.info_display.insert(END, "ID:\n" +
                                         str(user["id"]))

                # Display QR code
                self.qr_display.insert(END, text_QR_code(user["id"]))

                # Display Days attended
                self.info_display.insert(END, "\nDays Attended:")
                for day in user["days-attended"]:
                    if user["days-attended"][day] == True:
                        self.info_display.insert(END, "\n" + day)

                self.info_display.configure(state='disable')
                self.qr_display.configure(state='disable')
                break

    def remove_user(self):
        file_data = read_json()
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["name"] == self.member_list.get(ANCHOR):
                del file_data["members"][i]
                file_data["member-count"] -= 1
                break
        write_json(file_data)
        self.member_list.delete(ANCHOR)

    def reload_member_list(self):
        file_data = read_json()
        self.member_list.delete(0, END)
        unsorted_member_list = []
        for i in range(len(file_data["members"])):
            unsorted_member_list.append(file_data["members"][i]["name"])
        sorted_member_list = sorted(unsorted_member_list, key=str.lower)
        self.member_list.insert(END, *sorted_member_list)
