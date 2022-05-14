"""Data Input Module"""

import pandas as pd
from data_matching import DataMatching
from models import ConfigInfo


class DataInput:
    """DataInput class"""

    # parameterized constructor
    def __init__(self, config_info: ConfigInfo, user_interface):
        self.config_info = config_info
        self.data = None
        self.user_interface = user_interface

    def open_input_file(self):
        """This method is used to process the input file and exposing it as a data frame"""

        path = self.config_info.input_path

        try:
            if self.config_info.input_format == "csv":
                if self.config_info.input_format == "csv" and path.endswith(".csv"):
                    self.data = pd.read_csv(path)
                else:
                    error_message = "The input file does not match selected input file type - expected CSV file"
                    print(error_message)
                    self.user_interface.show_dialog(error_message)
                    return
            else:
                if self.config_info.input_format == "xlsx" and (path.endswith(".xls") or path.endswith(".xlsx")):
                    self.data = pd.read_excel(path)
                else:
                    error_message = "The input file does not match selected input file type - expected MS Excel file"
                    print(error_message)
                    self.user_interface.show_dialog(error_message)
                    return

            if len(self.data) == 0:
                error_message = "The input file does not contain the expected content..."
                print(error_message)
                self.user_interface.show_dialog(error_message)

            else:
                address_field = self.config_info.address_field
                if address_field in self.data.columns:
                    print("Data loaded successfully. Staring processing...")
                    data_matching = DataMatching(self.config_info, self.user_interface)
                    data_matching.process_input_records(self.data)
                else:
                    error_message = "Input file does not contain required {0} field.".format(
                        self.config_info.address_field)
                    print(error_message)
                    self.user_interface.show_dialog(error_message)

        except FileNotFoundError:
            error_message = "Error: File not found"
            print(error_message)
            self.user_interface.show_dialog(error_message)
