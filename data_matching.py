"""Data Matching Module"""
import sys
import requests
import pandas as pd
from models import APIResponseProperties, AddressDetails, ConfigInfo
from data_output import DataOutput


class DataMatching:
    """DataMatching class"""

    # parameterized constructor
    def __init__(self, config_info: ConfigInfo, user_interface):

        self.config_info = config_info

        self.output_records = None
        self.user_interface = user_interface

        user_interface.clear_ui()
        user_interface.update_gui()

    def process_input_records(self, input_records: pd.DataFrame):
        """This method receives a data frame from the input file and sends the processed data to the
        data output class"""

        self.user_interface.matching_in_progress = True

        if self.config_info.keep_all_input_fields:
            self.output_records = input_records
        else:
            self.output_records = input_records[[self.config_info.address_field]].copy()

        self.__amend_output_structure()

        for index, row in self.output_records.iterrows():

            if self.user_interface.matching_in_progress:
                query = row[self.config_info.address_field]
                processed_record = self.__process_record(query)
                row[APIResponseProperties.ADDRESS + "_M"] = processed_record.address
                row[APIResponseProperties.POSTCODE + "_M"] = processed_record.postcode
                row[APIResponseProperties.UPRN] = processed_record.uprn
                row[APIResponseProperties.X_COORDINATE] = processed_record.easting
                row[APIResponseProperties.Y_COORDINATE] = processed_record.northing
                row[APIResponseProperties.MATCH_SCORE] = processed_record.match_score
                row[APIResponseProperties.MATCH_DESCRIPTION] = processed_record.match_description
                self.__update_progress(index, len(self.output_records))
            else:
                break

        self.__print_summary()

        data_output = DataOutput(self.config_info, self.user_interface)
        data_output.save_output_file(self.output_records)

    def __update_progress(self, index, size):
        """This function updates the progress bar in the console.
        The code was adopted by modification of the solution
        provided here:
        https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
        We want to overwrite a line without going to the next line
        while drawing a progress bar and a status message...
        On this occasion sys.stdout.write is used.
        50 defines the number of characters we want to use in the progress bar."""

        if self.user_interface.matching_in_progress:
            sys.stdout.write('\r')
            j = (index + 1) / size
            sys.stdout.write("[%-50s] %d%%" % ('#' * int(50 * j), 100 * j))

            self.user_interface.info_label_text.set("%-100s" % ('#' * int(100 * j)))
            self.user_interface.info_label_text_p.set("Progress: %d%%" % (100 * j))
            self.user_interface.root.update()

    def __process_record(self, query):
        """This method is creating new AddressDetails instance and processing the verification"""
        address_record = AddressDetails()
        address_record.input_query = query
        address_record = self.__validate_address_record(address_record)

        return address_record

    def __amend_output_structure(self):
        """This method is adding new fields to existing data frame"""
        self.output_records[APIResponseProperties.ADDRESS + "_M"] = ""
        self.output_records[APIResponseProperties.POSTCODE + "_M"] = ""
        self.output_records[APIResponseProperties.UPRN] = ""
        self.output_records[APIResponseProperties.X_COORDINATE] = ""
        self.output_records[APIResponseProperties.Y_COORDINATE] = ""
        self.output_records[APIResponseProperties.MATCH_SCORE] = ""
        self.output_records[APIResponseProperties.MATCH_DESCRIPTION] = ""

    def __validate_address_record(self, address_details: AddressDetails):
        """This method process the input query and sends the validation request"""

        request_parameters = {"key": self.config_info.os_api_key,
                              "maxresults": self.config_info.os_api_max_results,
                              "query": address_details.input_query}

        url = str(self.config_info.os_api_url)
        response = requests.get(url=url, params=request_parameters)

        # extracting data in json format
        data = response.json()
        if isinstance(data, dict):
            if "fault" not in data.keys():
                if APIResponseProperties.RESULTS in data.keys():
                    if len(data[APIResponseProperties.RESULTS]) > 0:
                        address_m = data[APIResponseProperties.RESULTS][0]["DPA"]
                        address_details.address = address_m[APIResponseProperties.ADDRESS]
                        address_details.uprn = address_m[APIResponseProperties.UPRN]
                        address_details.easting = address_m[APIResponseProperties.X_COORDINATE]
                        address_details.northing = address_m[APIResponseProperties.Y_COORDINATE]
                        address_details.postcode = address_m[APIResponseProperties.POSTCODE]
                        address_details.match_score = address_m[APIResponseProperties.MATCH_SCORE]
                        if address_details.match_score > 0.5:
                            address_details.match_description = "MATCHED"
                        else:
                            address_details.match_description = "REVIEW REQUIRED"
                    else:
                        address_details.match_description = "REVIEW REQUIRED"
                else:
                    address_details.match_description = "REVIEW REQUIRED"
            else:
                address_details.match_description = "REVIEW REQUIRED"
        else:
            address_details.match_description = "REVIEW REQUIRED"
        return address_details

    def __print_summary(self):
        """This method print out the address matching summary."""

        no_of_records = len(self.output_records)
        matched = self.output_records[APIResponseProperties.MATCH_DESCRIPTION].value_counts()["MATCHED"]
        not_matched = no_of_records - matched

        print("\n")

        info1 = "{0} records processed".format(str(no_of_records))
        info2 = "{0} records has been matched".format(matched)
        info3 = "{0} records require review and manual resolution".format(not_matched)
        print(info1)
        print(info2)
        print(info3)

        self.user_interface.info_label_text_summary1.set(info1)
        self.user_interface.info_label_text_summary2.set(info2)
        self.user_interface.info_label_text_summary3.set(info3)
