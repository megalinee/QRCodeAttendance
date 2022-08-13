import tkinter as tk
import Constants as CONSTANT
from tkinter import ttk
from os.path import exists
from Tabs.AddMembers import AddMembersTab
from Tabs.ManageMembers import ManageMembersTab
from Tabs.Other import OtherTab


class Main:
    def __init__(self):
        # Checks if JSON exists, if not generates new JSON file
        if not exists(CONSTANT.pathToJSON):
            f = open(CONSTANT.pathToJSON, "a")
            f.write("{\"members\":[],\"member-count\": 0}")
            f.close()

        root = tk.Tk()
        root.title('Admin Dashboard')
        root.geometry("598x300")
        #root.resizable(False, False)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        tab_control = ttk.Notebook(root)

        manage_members = ManageMembersTab(tab_control)
        add_members = AddMembersTab(
            tab_control, manage_members.reload_member_list)
        other = OtherTab(tab_control)

        tab_control.add(manage_members, text='Manage Members')
        tab_control.add(add_members, text='Add Members')
        tab_control.add(other, text='Other')
        tab_control.pack(expand=1, fill="both")

        root.mainloop()


main = Main()
