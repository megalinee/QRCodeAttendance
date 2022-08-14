import tkinter as tk
import threading
import Constants as CONSTANT
from tkinter import ttk, Button, Label, filedialog, messagebox, Frame, CENTER
from Tools.JSONTools import read_json, write_json, json_to_csv, duplicate_json, create_json
from Scanner.Camera import Camera


class OtherTab(ttk.Frame):
    def __init__(self, parent, reload_member_list):
        super().__init__(parent)

        self.reload_member_list = reload_member_list

        self.generate_UI_components()

    def generate_UI_components(self):
        start_camera_button = Button(
            self, text='Start QR Scanner', command=self.start_camera_thread)
        start_camera_button.place(relx=.5, rely=.2, anchor=CENTER)

        # Export Buttons
        export_csv_button = Button(
            self, text='Export CSV', command=self.export_csv)
        export_csv_button.place(relx=.4, rely=.4, anchor=CENTER)

        export_json_button = Button(
            self, text='Export JSON', command=self.export_json)
        export_json_button.place(relx=.4, rely=.6, anchor=CENTER)

        import_json_button = Button(
            self, text='Import JSON', command=self.import_json)
        import_json_button.place(relx=.6, rely=.4, anchor=CENTER)

        reset_json_button = Button(
            self, text='Reset JSON', command=self.reset_json)
        reset_json_button.place(relx=.6, rely=.6, anchor=CENTER)

        self.status_label = Label(self, text="")
        self.status_label.place(relx=.5, rely=.75, anchor=CENTER)

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
            self.reload_member_list()
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
                self.reload_member_list()
                self.status_label.config(
                    text="Imported JSON file!")
