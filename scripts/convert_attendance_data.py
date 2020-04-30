import os
import csv
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# INITIALIZE CONSTANTS
CSV_NAME = 'Theta Tau App Spring 2020 Attendance.csv'
CSV_ID = '1aMVvVym0xSodK2cvmlinXbflfcTCcPvdqjl1_cE55Oo'
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)
OUTPUT_FILE_NAME = "2020-spring.json"
OUTPUT_FILE_PATH = GRANDPARENT_DIR + "/assets/js/" + OUTPUT_FILE_NAME

EMAIL_IDX = 0
DEFAULT_GM_IDX = 1
DEFAULT_OTHER_IDX = 2
EVENT_IDX = 3

EVENT_ROW_IDX = 1
DIVIDER_ROW_IDX = 15

CONFIG_LOOKUP = [
    "config",
    "type",
    "title",
    "description",
    "date",
    "time",
    "duration",
    "location",
    "mandatory",
    "excusable",
    "profPoints",
    "philPoints",
    "broPoints",
    "rushPoints",
    "anyPoints"
]

defaults = {
    'GM': {},
    'other': {}
}

data = {
    'events': []
}


def get_default(default_type, field_idx):
    if default_type in defaults:
        return defaults[default_type][field_idx]

    return defaults['other'][field_idx]


def get_drive():
    # AUTHENTICATE WITH GOOGLE
    os.chdir(PARENT_DIR)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    return GoogleDrive(gauth)


if __name__ == "__main__":
    DRIVE = get_drive()

    # DOWNLOAD CSV FILE
    GFILE = DRIVE.CreateFile({'id': CSV_ID})
    GFILE.GetContentFile(CSV_NAME, mimetype='text/csv')

    with open(CSV_NAME, 'r') as csvfile:
        READER = csv.reader(csvfile)

        for i, row in enumerate(READER):
            if i == 0:
                continue

            if i < DIVIDER_ROW_IDX:
                # Read defaults

                config_idx = CONFIG_LOOKUP[i]

                defaults['GM'][config_idx] = row[DEFAULT_GM_IDX]
                defaults['other'][config_idx] = row[DEFAULT_OTHER_IDX]

                # Read events
                for col_idx, col_value in enumerate(row):
                    if col_idx < EVENT_IDX:
                        # Skip configuration columns
                        continue

                    if i == EVENT_ROW_IDX:
                        # Add new event

                        data['events'].append({
                            'attended': [],
                            'excused': []
                        })

                    data_idx = col_idx - EVENT_IDX

                    # Get the event type already stored or currently being read
                    event_type = data['events'][data_idx]['type'] if 'type' in data['events'][data_idx] else col_value

                    # Write value if found or default value if applicable
                    data['events'][data_idx][config_idx] = col_value if col_value != "" else get_default(event_type, config_idx)

            elif i > DIVIDER_ROW_IDX:
                # Read attendance

                email = row[EMAIL_IDX]

                for col_idx, col_value in enumerate(row):
                    if col_idx < EVENT_IDX:
                        # Skip configuration columns
                        continue

                    data_idx = col_idx - EVENT_IDX

                    if col_value == "x":
                        data['events'][data_idx]['attended'].append(email)
                    elif col_value == "ex":
                        data['events'][data_idx]['excused'].append(email)

    # WRITE TO DATA
    with open(OUTPUT_FILE_PATH, 'w') as outfile:
        json.dump(data, outfile)

    print('Successfully updated', OUTPUT_FILE_NAME)
