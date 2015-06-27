import pytz
from datetime import datetime
from os import path
import json


def get_lots_from_json(city, lot_name):
    """
    Get the total value from the highest known value in the last saved JSON file.
    This is useful for cities that don't publish total number of spaces for a parking lot.

    Caveats:
     - Returns 0 if not found.
     - If a lot name exists twice only the last value is returned.

    :param city:
    :param lot_name:
    :return:
    """
    lots = 0
    last_values_json_path = path.join("cache", city + ".json")
    if path.isfile(last_values_json_path):
        with open(last_values_json_path) as data_file:
            last_values = json.load(data_file)
            if last_values is None:
                # if no last json file exists, return 0
                return 0
            for lastlots in last_values["lots"]:
                if lastlots["name"] is lot_name:
                    lots = int(lastlots["total"])
    return lots


def utc_now():
    """
    Returns the current UTC time in ISO format.

    :return:
    """
    return datetime.utcnow().replace(microsecond=0).isoformat()


def convert_date(date_string, date_format, timezone="Europe/Berlin"):
    """
    Convert a date into a ISO formatted UTC date string. Timezone defaults to Europe/Berlin.

    :param date_string:
    :param date_format:
    :param timezone:
    :return:
    """
    last_updated = datetime.strptime(date_string, date_format)
    local_timezone = pytz.timezone(timezone)
    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    return last_updated.replace(microsecond=0).isoformat()


def remove_special_chars(string):
    """
    Remove any umlauts, spaces and punctuation from a string.

    :param string:
    :return:
    """
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "-": "",
        " ": "",
        ".": "",
        ",": "",
        "'": "",
        "\"": ""
    }
    for repl in replacements.keys():
        string = string.replace(repl, replacements[repl])
    return string


def generate_id(city_file_path, lot_name):
    """
    Generate an ID for a parking lot by concatenating city name and lot name.

    :param city_file_path: __file__ for the city file
    :param lot_name: Name of the parking lot
    :return: ID
    """
    return remove_special_chars((path.basename(city_file_path)[:-3] + lot_name).lower())
