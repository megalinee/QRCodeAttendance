import tkinter as tk
import Constants as CONSTANT
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

        root = tk.Tk()
        root.title('Admin Dashboard')
        root.geometry(str(CONSTANT.window_x)+"x"+str(CONSTANT.window_y))
        root.resizable(False, False)

        tab_control = ttk.Notebook(root)

        manage_members = ManageMembersTab(tab_control)
        add_members = AddMembersTab(
            tab_control, manage_members.reload_member_list)
        other = OtherTab(tab_control, manage_members.reload_member_list)

        tab_control.add(manage_members, text='Manage Members')
        tab_control.add(add_members, text='Add Members')
        tab_control.add(other, text='Other')
        tab_control.pack(expand=1, fill="both")

        root.mainloop()


main = Main()
