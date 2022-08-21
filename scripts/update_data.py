import os
import sys
import csv
import pdb
import yaml
import argparse
from image_compress import compress_me
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# INITIALIZE CONSTANTS
CSV_NAME = 'Theta Tau Website Brother Info.csv'
CSV_ID = '1evBDIftoT8ZBg1jtLO6Wt_S6e0VNweqLC7J-fI0RmRM'
PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)
BROTHERS_IMG_LOCATION = "/assets/imgs/brothers/"
BROTHERS_IMG_DIR = GRANDPARENT_DIR + BROTHERS_IMG_LOCATION
MEMBERS_FILE_PATH = GRANDPARENT_DIR + "/_data/members.yml"
CLASS_IDX = 2
NAME_IDX = 3
MAJOR_IDX = 4
HOMETOWN_IDX = 5
LINKEDIN_IDX = 6
IMAGE_IDX = 7
ALUMNI_IDX = 8

data = {
    'actives': [
        {'semester': 'Spring 2022', 'members': []},
        {'semester': 'Fall 2021', 'members': []},
        {'semester': 'Spring 2021', 'members': []},
        {'semester': 'Fall 2020', 'members': []},
        {'semester': 'Spring 2020', 'members': []},
        {'semester': 'Fall 2019', 'members': []},
        {'semester': 'Spring 2019', 'members': []},
        {'semester': 'Fall 2018', 'members': []},
        {'semester': 'Spring 2018', 'members': []},
        {'semester': 'Fall 2017', 'members': []},
        {'semester': 'Spring 2017', 'members': []},
        {'semester': 'Fall 2016', 'members': []},
        {'semester': 'Spring 2016', 'members': []},
        {'semester': 'Fall 2015', 'members': []},
        {'semester': 'Spring 2015', 'members': []},
        {'semester': 'Fall 2014', 'members': []},
        {'semester': 'Spring 2014', 'members': []},
        {'semester': 'Fall 2013', 'members': []},
        {'semester': 'Spring 2013', 'members': []},
        {'semester': 'Fall 2012', 'members': []},
    ],
    'alumni': []
}


def index_of_class(pledge_class):
    # some error checking
    semester, year = pledge_class.split()
    if not semester in ('Fall', 'Spring'):
        print('Pledge class, {}, is wrong'.format(pledge_class))
        exit(1)

    for i in range(len(data['actives'])):
        if pledge_class == data['actives'][i]['semester']:
            return i
    return -1


def get_drive():
    # AUTHENTICATE WITH GOOGLE
    os.chdir(PARENT_DIR)
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    return drive


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
            semester = row[CLASS_IDX]
            name = row[NAME_IDX]
            major = row[MAJOR_IDX]
            hometown = row[HOMETOWN_IDX]
            linkedin = row[LINKEDIN_IDX]
            alumni = row[ALUMNI_IDX]

            print("Currently grabbing {}'s data!".format(name))

            # Check if we already processed it
            processed_name = name.lower().replace(' ', '_')
            processed_name = processed_name.lower().replace('(', '')
            processed_name = processed_name.lower().replace(')', '')
            if not os.path.isfile("{}{}{}".format(BROTHERS_IMG_DIR, processed_name, '.jpg')):
                if row[IMAGE_IDX]:
                    # CREATE GDRIVE FILE
                    gfile = drive.CreateFile({'id': row[IMAGE_IDX].split('=')[-1]})

                    # GET FILE
                    file_extension = '.{}'.format(gfile['title'].split('.')[-1])
                    pic_name = processed_name + file_extension.lower()  # generated file name
                    file_path = BROTHERS_IMG_DIR + pic_name  # absolute directory            

                    gfile.GetContentFile(file_path)
                    image_name = compress_me(os.path.join(BROTHERS_IMG_DIR, pic_name), jpeg=True, quality=85, dimension=450)[2]
                    print(image_name)
            else:
                image_name = processed_name + '.jpg'
                print('Already downloaded image for {}'.format(name))

            # Add check to ensure that linkedin starts with https://www. - otherwise link won't work

            # Create brother info dictionary
            if not row[IMAGE_IDX]:
                brother_data = {
                    'name': name,
                    'major': major,
                    'hometown': hometown,
                    'linkedin': linkedin,
                    'picture': os.path.join(BROTHERS_IMG_LOCATION, 'thetatau.jpg')
                }
            else:
                brother_data = {
                    'name': name,
                    'major': major,
                    'hometown': hometown,
                    'linkedin': linkedin,
                    'picture': os.path.join(BROTHERS_IMG_LOCATION, image_name)
                }

            if not alumni:
                # Add to 'actives' list. The for loop is needed to preserve ordering in the yaml file
                for pledge_class in data['actives']:
                    if semester in pledge_class['semester']:
                        if not any(brother['name'] == brother_data['name'] for brother in pledge_class['members']):
                            pledge_class['members'].append(brother_data)
                        break
                else:
                    print("WHAT?! This is only printing because the brother's semester data was not found")
                    exit(1)
            else:
                brother_data['pledge_class'] = semester
                data['alumni'].append(brother_data)

    data['alumni'].sort(key=lambda brother: index_of_class(brother['pledge_class']))

    # WRITE TO DATA
    with open(MEMBERS_FILE_PATH, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    print('Successfully updated members.yml and added images to {}'.format(BROTHERS_IMG_LOCATION))
