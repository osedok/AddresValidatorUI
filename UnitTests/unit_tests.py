"""Unit Testing module"""
import unittest
import requests
import models



class TestCoreImplementation(unittest.TestCase):
    """Creating a test class that inherits from the unittest.TestCase"""

    def test_good_quality_input(self):
        """Testing good quality input provided as ADDRESS field defined in the input file"""

        address_record = validate_record("Clarkston P.S. Nursery Class, 17 Findhorn Place Airdrie ML8 7HE")
        self.assertEqual(address_record.uprn, "118177859")
        self.assertEqual(address_record.match_description, "MATCHED")

    def test_bad_quality_input(self):
        """Testing bad quality input which could be provided as ADDRESS field defined in the input file"""

        # Input record above was modified (some typos included) - so address is no longer matched.
        # Review should be required
        address_record = validate_record("Claston P.S. Nursery Class, 17 Finbhorn Palace Airdrie ML8 7HE")
        self.assertEqual(address_record.match_description, "REVIEW REQUIRED")
        # Testing empty input - Review should be required
        address_record = validate_record("")
        self.assertEqual(address_record.match_description, "REVIEW REQUIRED")
        # Testing dummy input - Review should be required
        address_record = validate_record("dummy")
        self.assertEqual(address_record.match_description, "REVIEW REQUIRED")


def validate_record(query):
    """Function used by the data_matching module - this function is executed multiple times when the programme
        iterates through the input records."""

    config_info = models.ConfigInfo()

    address_record = models.AddressDetails()
    address_record.input_query = query

    request_parameters = {"key": config_info.os_api_key,
                          "maxresults": config_info.os_api_max_results,
                          "query": query}

    url = str(config_info.os_api_url)
    response = requests.get(url=url, params=request_parameters)

    # extracting data in json format
    data = response.json()
    if isinstance(data, dict):
        if "fault" not in data.keys():
            if models.APIResponseProperties.RESULTS in data.keys():
                if len(data[models.APIResponseProperties.RESULTS]) > 0:
                    address_m = data[models.APIResponseProperties.RESULTS][0]["DPA"]
                    address_record.address = address_m[models.APIResponseProperties.ADDRESS]
                    address_record.uprn = address_m[models.APIResponseProperties.UPRN]
                    address_record.easting = address_m[models.APIResponseProperties.X_COORDINATE]
                    address_record.northing = address_m[models.APIResponseProperties.Y_COORDINATE]
                    address_record.postcode = address_m[models.APIResponseProperties.POSTCODE]
                    address_record.match_score = address_m[models.APIResponseProperties.MATCH_SCORE]
                    if address_record.match_score > 0.5:
                        address_record.match_description = "MATCHED"
                    else:
                        address_record.match_description = "REVIEW REQUIRED"
                else:
                    address_record.match_description = "REVIEW REQUIRED"
            else:
                address_record.match_description = "REVIEW REQUIRED"
        else:
            address_record.match_description = "REVIEW REQUIRED"
    else:
        address_record.match_description = "REVIEW REQUIRED"

    return address_record
