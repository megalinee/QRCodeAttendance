import tkinter as tk
import customtkinter
import threading
import webbrowser
import Constants as CONSTANT
from tkinter import ttk, Button, Label, filedialog, messagebox, Frame, CENTER
from Tools.JSONTools import read_json, write_json, json_to_csv, duplicate_json, create_json
import os
from Tools.QRTools import generate_ID_card


class OtherTab(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.center = customtkinter.CTkFrame(
            parent, width=CONSTANT.window_x-25, height=CONSTANT.window_y-75)

        self.center.grid(row=0, sticky="nsew")

        self.generate_UI_components()

    def generate_UI_components(self):
        # Export Buttons
        export_csv_button = customtkinter.CTkButton(
            self.center, text='Export CSV', command=self.export_csv)
        export_csv_button.place(relx=.2, rely=.4, anchor=CENTER)

        export_json_button = customtkinter.CTkButton(
            self.center, text='Export JSON', command=self.export_json)
        export_json_button.place(relx=.2, rely=.6, anchor=CENTER)

        import_json_button = customtkinter.CTkButton(
            self.center, text='Import JSON', command=self.import_json)
        import_json_button.place(relx=.8, rely=.4, anchor=CENTER)

        reset_json_button = customtkinter.CTkButton(
            self.center, text='Reset JSON', command=self.reset_json)
        reset_json_button.place(relx=.8, rely=.6, anchor=CENTER)

        self.status_label = customtkinter.CTkLabel(self.center, text="")
        self.status_label.place(relx=.5, rely=.75, anchor=CENTER)

    def export_csv(self):
        path = filedialog.asksaveasfile(filetypes=[(
            'CSV File', '*.csv')], defaultextension=[(
                'CSV File', '*.csv')])
        if path != None:
            json_to_csv("data.json", path)
            self.status_label.configure(
                text="Generated file in this directory!")

    def export_json(self):
        path = filedialog.asksaveasfile(filetypes=[(
            'JSON File', '*.json')], defaultextension=[(
                'JSON File', '*.json')])
        if path != None:
            duplicate_json(path)
            self.status_label.configure(
                text="Generated file in this directory!")

    def reset_json(self):
        confirm = messagebox.askyesno(
            title='Confirmation', message='Are you sure that you want reset the JSON?\nDoing this will delete all saved data unless it was exported.')
        if confirm:
            create_json(CONSTANT.defaultJSON)
            self.status_label.configure(
                text="Reset JSON file!")

    def import_json(self):
        confirm = messagebox.askyesno(
            title='Confirmation', message='Are you sure that you want import another JSON?\nDoing this will change all data unless it was exported.')
        if confirm:
            path = filedialog.askopenfilename(filetypes=[(
                'JSON File', '*.json')], defaultextension=[(
                    'JSON File', '*.json')])
            if path != '':
                newjson = read_json(filename=path)
                write_json(newjson)
                for member in newjson["members"]:
                    generate_ID_card(member["Name"], member["ID"])
                self.status_label.config(
                    text="Imported JSON file!")

    def open_folder(self):
        if(os.path.exists("./IDcard")):
            webbrowser.open(os.path.abspath("./IDcard"))
        else:
            self.status_label.config(
                text="You must add at least 1 user!")
