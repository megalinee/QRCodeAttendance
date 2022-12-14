import tkinter as tk
import qrcode
import PIL
import customtkinter
import Constants as CONSTANT
from Tools.QRTools import generate_ID_card
from tkinter import ttk, Frame, Label, END, Button
from Tools.JSONTools import read_json, write_json


class AddMembersTab(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
        name_label = customtkinter.CTkLabel(
            self.ctr_left, text="Full Name", width=120)
        name_label.pack(pady=(20, 5), padx=3)

        self.full_name_var = tk.StringVar()
        name_entry = customtkinter.CTkEntry(
            self.ctr_left, textvariable=self.full_name_var, width=120)
        name_entry.pack()
        name_entry.focus()

        student_id_label = customtkinter.CTkLabel(
            self.ctr_left, text="Student ID", width=120)
        student_id_label.pack(pady=(20, 5))

        self.student_id_var = tk.StringVar()
        student_id_entry = customtkinter.CTkEntry(
            self.ctr_left, textvariable=self.student_id_var, width=120)
        student_id_entry.bind("<Return>", self.submit_user)
        student_id_entry.pack()
        student_id_entry.focus()

        submit_button = customtkinter.CTkButton(
            self.ctr_left, text='Submit', command=self.submit_user, width=100)
        submit_button.pack(pady=20, padx=0)

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
        self.info_display.insert(tk.END, "")
        self.info_display.configure(state='disable')

    def submit_user(self, event=None):
        # Get Full Name and Graduating Year
        full_name = str(self.full_name_var.get())
        student_id = str(self.student_id_var.get())

        # Update JSON
        file_data = read_json()
        file_data["members"].append({"ID": int(student_id),
                                    "Name": full_name,
                                     "days-attended": {

        }})
        file_data["member-count"] += 1
        write_json(file_data)

        generate_ID_card(full_name, student_id)

        # Update info boxes
        self.info_display.configure(state='normal')
        self.info_display.delete('1.0', END)

        qr = qrcode.make(int(student_id)).copy()
        qr_code = customtkinter.CTkImage(light_image=qr,
                                         dark_image=qr,
                                         size=(250, 250))
        self.qr_display.configure(image=qr_code)

        self.info_display.insert(tk.END, "Successfully added!\nName:\n" + full_name +
                                 "\nID:\n" + student_id)

        self.info_display.configure(state='disable')
