import os
import csv
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# INITIALIZE CONSTANTS
CSV_NAME = 'Theta Tau App Brother Info.csv'
# CSV_ID = '1MXKtTf_KFOHg08ljOexDXcSq6ONFkuaIfXdGoROtmZE'
CSV_ID = '1evBDIftoT8ZBg1jtLO6Wt_S6e0VNweqLC7J-fI0RmRM'
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)
DIRECTORY_FILE_PATH = GRANDPARENT_DIR + "/assets/js/directory.json"
EMAIL_IDX = 1
FIRST_YEAR_IDX = 2
PLEDGE_SEMESTER_IDX = 3
ROLE_IDX = 4
ALUMNI_IDX = 5
TEMP_FAMILY_NAME = 6
TEMP_GIVEN_NAME = 7

# PLEDGING = 'Spring 2020'
PLEDGING = 'Spring 2021'
# RUSHING = 'Fall 2020'
RUSHING = 'Fall 2021'

data = {
    'directory': {
        'active': {}
    }
}


def get_drive():
    # AUTHENTICATE WITH GOOGLE
    os.chdir(PARENT_DIR)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    return GoogleDrive(gauth)


if __name__ == "__main__":
    drive = get_drive()

    # DOWNLOAD CSV FILE
    gfile = drive.CreateFile({'id': CSV_ID})
    gfile.GetContentFile(CSV_NAME, mimetype='text/csv')

    with open(CSV_NAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            # GRAB DATA
            email = row[EMAIL_IDX]
            first_year = row[FIRST_YEAR_IDX]
            pledge_semester = row[PLEDGE_SEMESTER_IDX]
            role = row[ROLE_IDX]

            if pledge_semester != PLEDGING and pledge_semester != RUSHING:
                print("Currently grabbing {}'s data!".format(email))

                data['directory']['active'][email] = {
                    'firstYear': first_year,
                    'semester': pledge_semester,
                    'familyName': row[TEMP_FAMILY_NAME],
                    'givenName': row[TEMP_GIVEN_NAME]
                }

                if len(role) > 0:
                    data['directory']['active'][email]['role'] = role
                    data['directory']['active'][email]['privileged'] = True

    # WRITE TO DATA
    with open(DIRECTORY_FILE_PATH, 'w') as outfile:
        json.dump(data, outfile)

    print('Successfully updated directory.json')
