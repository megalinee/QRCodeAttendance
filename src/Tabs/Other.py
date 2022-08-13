import tkinter as tk
import threading
from tkinter import ttk, Button, Label, filedialog
from Tools.JSONTools import json_to_csv
from Scanner.Camera import Camera


class OtherTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.generate_UI_components()

    def generate_UI_components(self):
        start_camera_button = Button(
            self, text='Start QR Scanner', command=self.start_camera_thread)
        start_camera_button.pack(pady=5)

        export_csv_button = Button(
            self, text='Export CSV', command=self.export_csv)
        export_csv_button.pack(pady=5)
        self.export_csv_label = Label(self, text="")
        self.export_csv_label.pack()

    def start_camera_thread(self):
        camera = Camera()
        camera_thread = threading.Thread(target=camera.start)
        camera_thread.start()

    def export_csv(self):
        path = filedialog.asksaveasfile(filetypes=[(
            'CSV File', '*.csv')], defaultextension=[(
                'CSV File', '*.csv')])
        json_to_csv("data.json", path)
        self.export_csv_label.config(text="Generated file in this directory!")
