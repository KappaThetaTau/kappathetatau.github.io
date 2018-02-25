import os
import sys
import csv
import pdb
import yaml
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

CSV_NAME = 'Theta Tau Website Brother Info.csv'
CSV_ID = '1Cp0uUiHBa0amTX36_YrjFZLOwGNAN2ziry1dv7MymHY'
parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BROTHERS_IMG_FOLDER = parent_dir_name + "/assets/imgs/brothers/"
MEMBERS_FILE_PATH = parent_dir_name + "/_data/members.yml"

data = {
        'classes': [
            {
                'Fall 2017': []
                },
            {
                'Spring 2017': []
                },
            {
                'Fall 2016': []
                },
            {
                'Spring 2016': []
                },
            {
                'Fall 2015': []
                },
            {
                'Spring 2015': []
                },
            {
                'Fall 2014': []
                },
            {
                'Spring 2014': []
                },
            {
                'Fall 2013': []
                },
            {
                'Spring 2013': []
                },
            {
                'Fall 2012': []
                },
            ]
        }

CLASS_IDX = 2
NAME_IDX = 3
MAJOR_IDX = 4
HOMETOWN_IDX = 5
LINKEDIN_IDX = 6
IMAGE_IDX = 7

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Downlaod CSV file
gfile = drive.CreateFile({'id': CSV_ID})
gfile.GetContentFile(CSV_NAME, mimetype='text/csv')

with open(CSV_NAME, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        # GRAB DATA
        pledge_class = row[CLASS_IDX]
        name = row[NAME_IDX]
        major = row[MAJOR_IDX]
        hometown = row[HOMETOWN_IDX]
        linkedin = row[LINKEDIN_IDX]

        print "Currently grabbing {}'s data!".format(name)

        # CREATE GDRIVE FILE
        gfile = drive.CreateFile({'id': row[IMAGE_IDX].split('=')[-1]})

        # GET FILE
        file_extension = '.{}'.format(gfile['title'].split('.')[-1])
        pic_name = row[NAME_IDX].lower().replace(' ', '_') # generated file name
        file_name = BROTHERS_IMG_FOLDER + pic_name + file_extension # absolute directory
        gfile.GetContentFile(file_name)

        # ADD TO DATA
        for class_sem in data['classes']:
            if pledge_class in class_sem:
                '''Create the dictionary'''
                brother_data = {
                        'name': name,
                        'major': major,
                        'hometown': hometown,
                        'picture': pic_name + file_extension
                        }
                class_sem[pledge_class].append(brother_data)
                break
        else:
            print 'WHAT?!'
            exit(1)

with open(MEMBERS_FILE_PATH, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)

print 'Successfully updated members.yml and added images to /assets/imgs/brothers!'
