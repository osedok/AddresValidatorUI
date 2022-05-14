"""User Interface Module"""
import sys
import tkinter as tk
from tkinter import messagebox
from models import ConfigInfo
from data_input import DataInput


class UserInterface:
    """User Interface  class"""

    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Simple Address Validator")
        self.input_file_format = tk.StringVar()
        self.input_file_format.set("csv")
        self.output_file_format = tk.StringVar()
        self.output_file_format.set("csv")
        self.keep_all_input_fields = tk.IntVar()
        self.keep_all_input_fields.set(1)
        self.input_file = None
        self.input_address_field_name = None
        self.info_label_text = tk.StringVar()
        self.info_label_text.set("Progress Bar")
        self.info_label_text_p = tk.StringVar()
        self.info_label_text_p.set("Progress Percent")
        self.info_label_text_summary1 = tk.StringVar()
        self.info_label_text_summary1.set("")
        self.info_label_text_summary2 = tk.StringVar()
        self.info_label_text_summary2.set("")
        self.info_label_text_summary3 = tk.StringVar()
        self.info_label_text_summary3.set("")
        self.output_file_path = tk.StringVar()
        self.output_file_path.set("")

        self.matching_in_progress = False


    def show_dialog(self, message):
        messagebox.showinfo("Warning", message)

    def start_matching_process(self):
        self.root.update()

        if len(self.input_file.get()) == 0:
            self.show_dialog("Please enter the path to the input file")
            return

        config_info = ConfigInfo()
        config_info.input_path = self.input_file.get()
        config_info.input_format = self.input_file_format.get()
        config_info.output_format = self.output_file_format.get()
        config_info.address_field = self.input_address_field_name.get()
        config_info.keep_all_input_fields = self.keep_all_input_fields.get()
        data_input = DataInput(config_info, self)
        data_input.open_input_file()

    def set_ui(self):
        info_label = tk.Label(self.root, text="This program is a tool to match input address records with OS API Addressbase product.", padx=20, pady=20, justify=tk.LEFT)
        frame1 = tk.LabelFrame(self.root, text="Select Input File Format", padx=10, pady=10)
        frame2 = tk.LabelFrame(self.root, text="Input File", padx=10, pady=10)
        frame3 = tk.LabelFrame(self.root, text="Address Field", padx=10, pady=10)
        frame4 = tk.LabelFrame(self.root, text="Select Output File Format", padx=10, pady=10)

        radio_button1 = tk.Radiobutton(frame1, text="File format csv", variable=self.input_file_format, value="csv")
        radio_button2 = tk.Radiobutton(frame1, text="File format MS Excel", variable=self.input_file_format, value="xlsx")

        radio_button3 = tk.Radiobutton(frame4, text="File format csv", variable=self.output_file_format, value="csv")
        radio_button4 = tk.Radiobutton(frame4, text="File format MS Excel", variable=self.output_file_format, value="xlsx")

        self.input_file = tk.Entry(frame2, width=60)
        self.input_file.insert(0, r"/Users/osedok/PycharmProjects/AddresValidatorUI/Input/input.csv")

        self.input_address_field_name = tk.Entry(frame3)
        self.input_address_field_name.insert(0, "Address")

        start_matching_button = tk.Button(self.root, text="Match Records", command=self.start_matching_process)
        start_matching_button.grid(row=19, column=19, padx=20, pady=20)

        info_label.grid(row=0, column=0, columnspan=20)

        frame1.grid(row=1, column=0, padx=20, sticky=tk.W)
        radio_button1.grid(row=0, column=0, sticky=tk.W)
        radio_button2.grid(row=1, column=0, sticky=tk.W)

        frame4.grid(row=1, column=1, padx=20, sticky=tk.W)
        radio_button3.grid(row=0, column=0, sticky=tk.W)
        radio_button4.grid(row=1, column=0, sticky=tk.W)

        frame2.grid(row=2, column=0, padx=20, pady=20, columnspan=20, sticky=tk.W)
        self.input_file.grid(row=0, column=0)

        frame3.grid(row=3, column=0, padx=20, sticky=tk.W)
        self.input_address_field_name.grid(row=0, column=0)

        keep_all = tk.Checkbutton(self.root, text="Keep All Input Fields", variable=self.keep_all_input_fields, onvalue=1, offvalue=0, height=5, width=16)
        keep_all.grid(row=1, column=3, padx=20, pady=20)

        self.root.mainloop()


    def clear_ui(self):
        widgets = self.root.grid_slaves()
        for widget in widgets:
            widget.destroy()
        self.root.update()

    def update_gui(self):

        self.root.geometry('830x310')
        self.root.protocol('WM_DELETE_WINDOW', lambda :self.exit_program(True))

        tk.Label(self.root, textvariable=self.info_label_text, width=100, anchor=tk.W).grid(row=1, column=0, columnspan=20, sticky=tk.W, padx=10, pady=20)
        tk.Label(self.root, textvariable=self.info_label_text_p, width=15, anchor=tk.W).grid(row=2, column=0, columnspan=20, rowspan=2, sticky=tk.W, padx=10, pady=20)
        tk.Label(self.root, textvariable=self.info_label_text_summary1, anchor=tk.W, width=30).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.root, textvariable=self.info_label_text_summary2, anchor=tk.W, width=30).grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.root, textvariable=self.info_label_text_summary3, anchor=tk.W, width=50).grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.root, textvariable=self.output_file_path, anchor=tk.W, width=50).grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)

        tk.Button(self.root, text='Stop Processing', command=lambda :self.exit_program(False)).grid(row=10, column=14, padx=10, pady=10, sticky=tk.W, rowspan=6)
        self.root.update()

    def exit_program(self, close_window):

        self.matching_in_progress = False

        for widget in self.root.grid_slaves():
            if widget.winfo_name() == "!button2":
                widget.destroy()
                break
        self.root.update()

        if close_window:
            self.root.quit()
            sys.exit(0)
