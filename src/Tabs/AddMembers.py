import tkinter as tk
import Constants as CONSTANT
from Tools.QRTools import text_QR_code, generate_ID_card
from tkinter import ttk, Frame, Label, END, Button
from Tools.JSONTools import read_json, write_json


class AddMembersTab(ttk.Frame):
    def __init__(self, parent, reload_member_list):
        super().__init__(parent)
        self.reload_member_list = reload_member_list

        center = Frame(self, bg='black', width=100, height=200)

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
        name_label = Label(self.ctr_left, text="Full Name")
        name_label.pack(pady=(20, 5))

        self.full_name_var = tk.StringVar()
        name_entry = ttk.Entry(self.ctr_left, textvariable=self.full_name_var)
        name_entry.pack()
        name_entry.focus()

        student_id_label = Label(self.ctr_left, text="Student ID")
        student_id_label.pack(pady=(20, 5))

        self.student_id_var = tk.StringVar()
        student_id_entry = ttk.Entry(
            self.ctr_left, textvariable=self.student_id_var)
        student_id_entry.pack()
        student_id_entry.focus()

        submit_button = Button(
            self.ctr_left, text='Submit', command=self.submit_user)
        submit_button.pack(pady=20)

        self.qr_display = tk.Text(self.ctr_right, height=15, width=30)
        self.qr_display.configure(state='disable')
        self.qr_display.pack(pady=15, padx=(5, 10))

        self.info_display = tk.Text(self.ctr_mid, height=15, width=20)
        self.info_display.pack(pady=15, padx=(10, 5))
        self.info_display.insert(tk.END, "")
        self.info_display.configure(state='disable')

    def submit_user(self):
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
        self.qr_display.configure(state='normal')
        self.qr_display.delete('1.0', END)

        self.info_display.insert(tk.END, "Successfully added!\nName:\n" + full_name +
                                 "\nID:\n" + student_id)
        self.qr_display.insert(tk.END, text_QR_code(int(student_id)))

        self.info_display.configure(state='disable')
        self.qr_display.configure(state='disable')

        self.reload_member_list()
