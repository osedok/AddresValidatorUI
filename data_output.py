"""Data Output Module"""
import os
import pandas as pd
from models import ConfigInfo


class DataOutput:
    """DataOutput class"""

    # parameterized constructor
    def __init__(self, config_info: ConfigInfo, user_interface):
        self.input_file_name = "output"
        self.config_info = config_info
        self.user_interface = user_interface

    def save_output_file(self, output_records: pd.DataFrame):
        """This method is used to save the output file.
        The required output format can be set in the config file.
        """

        output_directory = "Output"
        output_extension = self.config_info.output_format
        output_file_name = self.input_file_name + "." + output_extension
        path = os.path.join(output_directory, output_file_name)

        if str(output_extension).lower() == "csv":
            output_records.to_csv(path, index=False)
        if str(output_extension).lower() == "xlsx":
            output_records.to_excel(path, index=False)

        output_info = "The output file: " + path + " has been generated."
        print(output_info)
        self.user_interface.output_file_path.set(output_info)
        self.user_interface.exit_program(False)

