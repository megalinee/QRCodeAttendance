import tkinter as tk
import threading
import webbrowser
import Constants as CONSTANT
from tkinter import ttk, Button, Label, filedialog, messagebox, Frame, CENTER
from Tools.JSONTools import read_json, write_json, json_to_csv, duplicate_json, create_json
import os
from Scanner.Camera import Camera


class OtherTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.generate_UI_components()

    def generate_UI_components(self):
        start_camera_button = Button(
            self, text='Start QR Scanner', command=self.start_camera_thread)
        start_camera_button.place(relx=.5, rely=.1, anchor=CENTER)

        # Export Buttons
        export_csv_button = Button(
            self, text='Export CSV', command=self.export_csv)
        export_csv_button.place(relx=.4, rely=.3, anchor=CENTER)

        export_json_button = Button(
            self, text='Export JSON', command=self.export_json)
        export_json_button.place(relx=.4, rely=.5, anchor=CENTER)

        import_json_button = Button(
            self, text='Import JSON', command=self.import_json)
        import_json_button.place(relx=.6, rely=.3, anchor=CENTER)

        reset_json_button = Button(
            self, text='Reset JSON', command=self.reset_json)
        reset_json_button.place(relx=.6, rely=.5, anchor=CENTER)

        open_id_folder = Button(
            self, text='Open ID Badges', command=self.open_folder)
        open_id_folder.place(relx=.5, rely=.7, anchor=CENTER)

        self.status_label = Label(self, text="")
        self.status_label.place(relx=.5, rely=.85, anchor=CENTER)

    def start_camera_thread(self):
        camera = Camera()
        camera_thread = threading.Thread(target=camera.start)
        camera_thread.start()

    def export_csv(self):
        path = filedialog.asksaveasfile(filetypes=[(
            'CSV File', '*.csv')], defaultextension=[(
                'CSV File', '*.csv')])
        if path != None:
            json_to_csv("data.json", path)
            self.status_label.config(
                text="Generated file in this directory!")

    def export_json(self):
        path = filedialog.asksaveasfile(filetypes=[(
            'JSON File', '*.json')], defaultextension=[(
                'JSON File', '*.json')])
        if path != None:
            duplicate_json(path)
            self.status_label.config(
                text="Generated file in this directory!")

    def reset_json(self):
        confirm = messagebox.askyesno(
            title='Confirmation', message='Are you sure that you want reset the JSON?\nDoing this will delete all saved data unless it was exported.')
        if confirm:
            create_json(CONSTANT.defaultJSON)
            self.status_label.config(
                text="Reset JSON file!")

    def import_json(self):
        confirm = messagebox.askyesno(
            title='Confirmation', message='Are you sure that you want import another JSON?\nDoing this will change all data unless it was exported.')
        if confirm:
            path = filedialog.askopenfilename(filetypes=[(
                'JSON File', '*.json')], defaultextension=[(
                    'JSON File', '*.json')])
            if path != '':
                write_json(read_json(filename=path))
                self.status_label.config(
                    text="Imported JSON file!")

    def open_folder(self):
        if(os.path.exists("./IDcard")):
            webbrowser.open(os.path.abspath("./IDcard"))
        else:
            self.status_label.config(
                text="You must add at least 1 user!")
