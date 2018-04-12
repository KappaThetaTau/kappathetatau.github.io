#run this in any directory add -v for verbose 
#get Pillow (fork of PIL) from pip before running --> pip install Pillow

import os
import pdb
import sys
import ntpath
from PIL import Image

COMPRESS_DIMENSION = 256
COMPRESS_QUALITY = 50
IMG_DIR = '/assets/imgs/companies/'

def compress_me(file, path, verbose=False, jpeg=False):
    # convert to jpg
    if jpeg:
        filepath = convert_to_jpg(os.path.join(path, file))
    else:
        filepath = os.path.join(path, file)

    # Grab picture and metadata
    oldsize = os.stat(filepath).st_size
    picture = Image.open(filepath)
    dim = picture.size

    #set quality= to the preferred quality. 
    #I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
    picture.thumbnail((COMPRESS_DIMENSION,COMPRESS_DIMENSION))
    if jpeg:
        picture.save(filepath,"JPEG",optimize=True,quality=COMPRESS_QUALITY)
    else:
        picture.save(filepath,optimize=True,quality=COMPRESS_QUALITY)

    newsize = os.stat(filepath).st_size
    percent = (oldsize-newsize)/float(oldsize)*100
    if (verbose):
        print "File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent)
    return percent, filepath, path_leaf(filepath)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def convert_to_jpg(filepath):
    f, e = os.path.splitext(filepath)
    outfile = f + ".jpg"
    # We don't want to delete .JPG or .JPEG so we lower the extension
    filepath_lowered = f + e.lower()
    if outfile != filepath_lowered: 
        try:
            Image.open(filepath).convert('RGB').save(outfile)
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
