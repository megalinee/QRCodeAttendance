import tkinter as tk
import qrcode
import PIL
import customtkinter
import Constants as CONSTANT
from tkinter import ttk, Frame, Listbox, END, ANCHOR, Button, StringVar, Entry
from Tools.JSONTools import read_json, write_json


class ManageMembersTab(customtkinter.CTkFrame):
    def __init__(self, parent, tabcontrol):
        super().__init__(parent)
        self.parent = parent
        self.tabcontrol = tabcontrol

        center = customtkinter.CTkFrame(
            parent, width=100, height=200)

        center.grid(row=0, sticky="nsew")

        self.ctr_left = customtkinter.CTkFrame(
            center, width=100, height=190, corner_radius=0)
        self.ctr_mid = customtkinter.CTkFrame(
            center, width=100, height=190, corner_radius=0)
        self.ctr_right = customtkinter.CTkFrame(
            center, width=100, height=190, corner_radius=0)
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_mid.grid(row=0, column=1, sticky="ns")
        self.ctr_right.grid(row=0, column=2, sticky="ns")

        self.generate_UI_components()

    def generate_UI_components(self):
        self.search_str = StringVar()
        self.search = customtkinter.CTkEntry(
            self.ctr_left, textvariable=self.search_str, width=120)
        self.search.pack(pady=(20, 0))
        self.search.bind('<Return>', self.filter_member_list)

        self.member_list = Listbox(self.ctr_left, activestyle="none")
        self.member_list.bind('<Double-1>', self.select_user)
        self.member_list.pack(pady=(10, 15), padx=1)

        # Update when tab is changed.
        self.reload_member_list()
        self.tabcontrol.configure(command=self.reload_member_list)

        qr_placeholder = PIL.Image.new(mode="RGB", size=(250, 250),
                                       color=(255, 255, 255))
        qr_code = customtkinter.CTkImage(light_image=qr_placeholder,
                                         dark_image=qr_placeholder,
                                         size=(250, 250))
        self.qr_display = customtkinter.CTkLabel(self.ctr_right,
                                                 image=qr_code,
                                                 fg_color="transparent",
                                                 text="")
        self.qr_display.pack(pady=15, padx=(5, 2))

        self.info_display = customtkinter.CTkTextbox(
            self.ctr_mid, height=250, width=175)
        self.info_display.pack(pady=15, padx=(10, 5))
        self.info_display.insert(tk.END, "ID:\nDays Attended:")
        self.info_display.configure(state='disable')

        delete_button = customtkinter.CTkButton(
            self.ctr_left, text='Delete', command=self.remove_user, width=100)
        delete_button.pack()

    def select_user(self, event=None):
        file_data = read_json()
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["Name"] == self.member_list.get(ANCHOR):
                user = file_data["members"][i]
                self.info_display.configure(state='normal')
                self.info_display.delete('1.0', END)

                # Display ID
                self.info_display.insert(END, "ID:\n" +
                                         str(user["ID"]))

                # Display QR code
                qr = qrcode.make(user["ID"]).copy()
                qr_code = customtkinter.CTkImage(light_image=qr,
                                                 dark_image=qr,
                                                 size=(250, 250))
                self.qr_display.configure(image=qr_code)

                # Display Days attended
                self.info_display.insert(END, "\nDays Attended:\n")
                attended = False
                for day in user["days-attended"]:
                    if user["days-attended"][day] != 0:
                        attended = True
                        self.info_display.insert(
                            END, "----------\n" + day + "\n" + str(int(user["days-attended"][day])) + " min\n")
                if attended:
                    self.info_display.insert(END, "----------")

                self.info_display.configure(state='disable')
                break

    def remove_user(self):
        file_data = read_json()
        for i in range(len(file_data["members"])):
            if file_data["members"][i]["Name"] == self.member_list.get(ANCHOR):
                del file_data["members"][i]
                file_data["member-count"] -= 1
                break
        write_json(file_data)
        self.member_list.delete(ANCHOR)

    def reload_member_list(self, event=None):
        file_data = read_json()
        self.member_list.delete(0, END)
        unsorted_member_list = []
        for i in range(len(file_data["members"])):
            unsorted_member_list.append(file_data["members"][i]["Name"])
        sorted_member_list = sorted(unsorted_member_list, key=str.lower)
        self.member_list.insert(END, *sorted_member_list)

    def filter_member_list(self, event=None):
        file_data = read_json()
        self.member_list.delete(0, END)
        unsorted_member_list = []
        for i in range(len(file_data["members"])):
            if (self.search_str.get().lower() in file_data["members"][i]["Name"].lower()):
                unsorted_member_list.append(file_data["members"][i]["Name"])
        sorted_member_list = sorted(unsorted_member_list, key=str.lower)
        self.member_list.insert(END, *sorted_member_list)
