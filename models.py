"""Data Models Module"""
from strenum import StrEnum



class ConfigInfo:
    """This class is used to store the details of the configuration provided by user"""

    def __init__(self):
        self.input_format = "csv"
        self.output_format = "csv"
        self.input_path = ""
        self.address_field = "Address"
        self.keep_all_input_fields = 1
        self.os_api_url = "https://api.os.uk/search/places/v1/find"
        self.os_api_key = ""
        self.os_api_max_results = 1


class Point:
    """This class is used to store the details of the geometry (POINT) coordinates"""

    def __init__(self):
        self.easting = 0.0
        self.northing = 0.0


class AddressDetails(Point):
    """This class is used to store the details of the output record"""

    def __init__(self):

        self.uprn = ""
        self.address = ""
        self.postcode = ""
        self.match_score = 0
        self.match_description = ""
        self.input_query = ""


class APIResponseProperties(StrEnum):
    """This Enum class is used to access properties of JSON response from OS Data Hub API request.
    Instead of hard coding these properties they will be used as static values
    included in this class."""

    HEADER = 'header'
    RESULTS = 'results'
    QUERY = 'query'
    UPRN = 'UPRN'
    ADDRESS = 'ADDRESS'
    POSTCODE = 'POSTCODE'
    X_COORDINATE = 'X_COORDINATE'
    Y_COORDINATE = 'Y_COORDINATE'
    MATCH_SCORE = 'MATCH'
    MATCH_DESCRIPTION = "MATCH_DESCRIPTION"
