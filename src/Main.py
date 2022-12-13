import tkinter as tk
import customtkinter
import Constants as CONSTANT
from customtkinter import CTk
from Tools.JSONTools import create_json
from tkinter import ttk
from os.path import exists
from Tabs.AddMembers import AddMembersTab
from Tabs.ManageMembers import ManageMembersTab
from Tabs.Other import OtherTab


class Main:
    def __init__(self):
        # Checks if JSON exists, if not generates new JSON file
        if not exists(CONSTANT.pathToJSON):
            create_json(CONSTANT.defaultJSON)

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        root = customtkinter.CTk()
        root.title('Admin Dashboard')
        root.geometry(str(CONSTANT.window_x)+"x"+str(CONSTANT.window_y))
        root.resizable(False, False)

        tab_control = customtkinter.CTkTabview(root)

        manage_members = tab_control.add("Manage Members")
        add_members = tab_control.add("Add Members")
        other = tab_control.add("Other")

        ManageMembersTab(manage_members, tab_control)
        AddMembersTab(add_members)
        OtherTab(other)

        tab_control.set("Manage Members")

        tab_control.pack()

        root.mainloop()


main = Main()
