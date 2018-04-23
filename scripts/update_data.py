import os
import sys
import csv
import pdb
import yaml
from image_compress import compress_me
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# INITIALIZE CONSTANTS
CSV_NAME = 'Theta Tau Website Brother Info.csv'
CSV_ID = '1Cp0uUiHBa0amTX36_YrjFZLOwGNAN2ziry1dv7MymHY'
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

data = {
        'classes': [
            { 'semester': 'Spring 2018', 'members': [] },
            { 'semester': 'Fall 2017', 'members': [] },
            { 'semester': 'Spring 2017', 'members': [] },
            { 'semester': 'Fall 2016', 'members': [] },
            { 'semester': 'Spring 2016', 'members': [] },
            { 'semester': 'Fall 2015', 'members': [] },
            { 'semester': 'Spring 2015', 'members': [] },
            { 'semester': 'Fall 2014', 'members': [] },
            { 'semester': 'Spring 2014', 'members': [] },
            { 'semester': 'Fall 2013', 'members': [] },
            { 'semester': 'Spring 2013', 'members': [] },
            { 'semester': 'Fall 2012', 'members': [] },
            ]
        }

# AUTHENTICATE WITH GOOGLE
os.chdir(PARENT_DIR)
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# DOWNLOAD CSV FILE
gfile = drive.CreateFile({'id': CSV_ID})
gfile.GetContentFile(CSV_NAME, mimetype='text/csv')

with open(CSV_NAME, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        # GRAB DATA
        semester = row[CLASS_IDX]
        name = row[NAME_IDX]
        major = row[MAJOR_IDX]
        hometown = row[HOMETOWN_IDX]
        linkedin = row[LINKEDIN_IDX]

        print "Currently grabbing {}'s data!".format(name)

        # CREATE GDRIVE FILE
        gfile = drive.CreateFile({'id': row[IMAGE_IDX].split('=')[-1]})

        # GET FILE
        file_extension = '.{}'.format(gfile['title'].split('.')[-1])
        pic_name = row[NAME_IDX].lower().replace(' ', '_') + file_extension # generated file name
        file_path = BROTHERS_IMG_DIR + pic_name # absolute directory
        gfile.GetContentFile(file_path)

        # COMPRESS IMAGE
        image_name = compress_me(pic_name, BROTHERS_IMG_DIR, jpeg=True, quality=85, dimension=450)[2]

        # ADD TO DATA
        for pledge_class in data['classes']:
            if semester in pledge_class['semester']:
                '''Create the dictionary'''
                brother_data = {
                        'name': name,
                        'major': major,
                        'hometown': hometown,
                        'linkedin': linkedin,
                        'picture': os.path.join(BROTHERS_IMG_LOCATION, image_name)
                        }
                pledge_class['members'].append(brother_data)
                break
        else:
            print 'WHAT?!'
            exit(1)

# WRITE TO DATA
with open(MEMBERS_FILE_PATH, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

print 'Successfully updated members.yml and added images to {}'.format(BROTHERS_IMG_LOCATION)
