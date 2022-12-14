import tkinter as tk
import customtkinter
import threading
import Constants as CONSTANT
from tkinter import ttk, Button, Label, filedialog, messagebox, Frame, CENTER
from Tools.JSONTools import read_json, write_json, json_to_csv, duplicate_json, create_json
from Scanner.Camera import Camera


class ScannerTab(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.center = customtkinter.CTkFrame(
            parent, width=CONSTANT.window_x-25, height=CONSTANT.window_y-75)

        self.center.grid(row=0, sticky="nsew")

        self.generate_UI_components()

    def generate_UI_components(self):
        start_camera_button = customtkinter.CTkButton(
            self.center, text='Start QR Scanner', command=self.start_camera_thread)
        start_camera_button.place(relx=.5, rely=.2, anchor=CENTER)

    def start_camera_thread(self):
        camera = Camera()
        camera_thread = threading.Thread(target=camera.start)
        camera_thread.start()
