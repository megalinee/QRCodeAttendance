import os
import tkinter as tk
import webbrowser
import customtkinter
from os.path import exists
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

        self.switch_var = customtkinter.StringVar(value="off")

        if exists('config.txt'):
            with open(os.path.abspath("./config.txt"),'r') as f:
                self.switch_var.set(f.read())
        else:
            with open(os.path.abspath("./config.txt"),'w') as f:
                f.write(self.switch_var.get())

        self.generate_UI_components()

    def generate_UI_components(self):
        start_camera_button = customtkinter.CTkButton(
            self.center, text='Start QR Scanner', command=self.start_camera_thread)
        start_camera_button.place(relx=.5, rely=.2, anchor=CENTER)
        
        switch_1 = customtkinter.CTkSwitch(self.center, text="Enable Picture Saving", command=self.enable_picture_save,
                                   variable=self.switch_var, onvalue="on", offvalue="off")
        switch_1.place(relx=.5, rely=.5, anchor=CENTER)
        
        open_id_folder = customtkinter.CTkButton(self.center,
                                                 text='Open Saved Pictures',
                                                 command=self.open_folder,
                                                 fg_color="#db7100",
                                                 hover_color="#b85900")
        open_id_folder.place(relx=.5, rely=.7, anchor=CENTER)
        
        self.status_label = customtkinter.CTkLabel(self.center, text="")
        self.status_label.place(relx=.5, rely=.9, anchor=CENTER)
        
        

    def start_camera_thread(self):
        camera = Camera(pictureMode=self.switch_var.get())
        camera_thread = threading.Thread(target=camera.start)
        camera_thread.start()
        
    def enable_picture_save(self):
        if not exists("./ScanPictures") and self.switch_var.get() == "on":
            os.mkdir("./ScanPictures")
        with open(os.path.abspath("./config.txt"),'w') as f:
                f.write(self.switch_var.get())
    
    def open_folder(self):
        if (os.path.exists("./ScanPictures")):
            webbrowser.open(os.path.abspath("./ScanPictures"))
        else:
            self.status_label.configure(
                text="You must enable picture saving first!")
