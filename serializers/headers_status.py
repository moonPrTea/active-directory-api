from enum import Enum

class HeadersStatus(str, Enum):
    UNKNOWN_HEADER = "Unknow header value"
    VALID_HEADER = "Header value is valid"
