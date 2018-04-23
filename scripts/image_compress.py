#run this in any directory add -v for verbose 
#get Pillow (fork of PIL) from pip before running --> pip install Pillow

import os
import pdb
import sys
import ntpath
from PIL import Image, ExifTags

COMPRESS_DIMENSION = 450
COMPRESS_QUALITY = 85
IMG_DIR = '/scripts/test'

def compress_me(file, path, verbose=False, jpeg=False, quality=COMPRESS_QUALITY, dimension=COMPRESS_DIMENSION):
    # convert to jpg
    if jpeg:
        file_path = convert_to_jpg(os.path.join(path, file))
    else:
        file_path = os.path.join(path, file)

    # Grab picture and metadata
    oldsize = os.stat(file_path).st_size
    image = Image.open(file_path)

    #set quality= to the preferred quality. 
    #I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
    image.thumbnail((dimension,dimension))
    if jpeg:
        image.save(file_path,"JPEG",optimize=True,quality=quality)
    else:
        image.save(file_path,optimize=True,quality=quality)

    newsize = os.stat(file_path).st_size
    percent = (oldsize-newsize)/float(oldsize)*100
    if (verbose):
        print "File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent)
    return percent, file_path, path_leaf(file_path)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def convert_to_jpg(filepath):
    """ If file is not extended by .jpg then it saves it as .jpg from either
    .jpeg or .png This function also rotates the image before saving it since
    saving the image deletes all EXIF metadata. """

    f, e = os.path.splitext(filepath)
    outfile = f + ".jpg"
    # We don't want to delete .JPG or .JPEG so we lower the extension
    filepath_lowered = f + e.lower()
    if outfile != filepath_lowered: 
        try:
            image = Image.open(filepath)

            # Rotate image: https://stackoverflow.com/a/6218425
            # for orientation in ExifTags.TAGS.keys() : 
                # if ExifTags.TAGS[orientation] == 'Orientation' : break 
            orientation = 274  # get 274 through upper loop
            try:
                exif=dict(image._getexif().items())
                print exif[orientation]
                if exif[orientation] == 3 : 
                    image=image.rotate(180, expand=True)
                elif exif[orientation] == 6 : 
                    image=image.rotate(270, expand=True)
                elif exif[orientation] == 8 : 
                    image=image.rotate(90, expand=True)
            except (AttributeError, KeyError): # image has no meta data
                pass

            image.convert('RGB').save(outfile)
        except IOError:
            print("cannot convert", filepath)
            exit(1)
        os.remove(filepath)
        return outfile
    return filepath

def main():
    verbose = False
    #checks for verbose flag
    if (len(sys.argv)>1):
            if (sys.argv[1].lower()=="-v"):
                    verbose = True

    #find image directory
    grandpa = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    img_dir = grandpa + IMG_DIR

    tot = 0
    num = 0
    for directory, subdirectories, files in os.walk(img_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png'):
                    num += 1
                    percent, filepath, file = compress_me(file, img_dir, verbose)
                    tot += percent
    print "Average Compression: %d" % (float(tot)/num)
    print "Done"

if __name__ == "__main__":
    main()
