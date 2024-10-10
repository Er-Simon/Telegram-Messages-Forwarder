# Datetime format
# Set the format for displaying date and time
# Examples:
# '%Y-%m-%d %H:%M:%S' -> '2023-09-20 15:30:45'
# '%d/%m/%Y %I:%M %p' -> '20/09/2023 03:30 PM'
DATETIME_FORMAT = '%d-%m-%Y_%H-%M-%S'
#
# Timezone settings
# List of valid timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONE_NAME = 'Europe/Rome'
import pytz
TZ_INFO = pytz.timezone(TIMEZONE_NAME)


DATA_FOLDER_NAME = "data"
CONFIG_FILE_NAME = "config.json"
SESSION_FILE_NAME = "{}"

LOGS_FOLDER_NAME = "logs"
LOG_FILE_NAME = "{}.log"

import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER_PATH = os.path.join(DIR_PATH, DATA_FOLDER_NAME)
CONFIG_FILE_PATH = os.path.join(DATA_FOLDER_NAME, CONFIG_FILE_NAME)
SESSION_FILE_PATH = os.path.join(DATA_FOLDER_NAME, SESSION_FILE_NAME)


LOGS_FOLDER_PATH = os.path.join(DIR_PATH, LOGS_FOLDER_NAME)
LOG_FILE_PATH = os.path.join(LOGS_FOLDER_PATH, LOG_FILE_NAME)