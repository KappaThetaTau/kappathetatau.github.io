#run this in any directory add -v for verbose 
#get Pillow (fork of PIL) from pip before running --> pip install Pillow

import os
import pdb
import sys
import ntpath
import argparse
from PIL import Image, ExifTags

def compress_me(file_path, verbose=False, jpeg=False, quality=85, dimension=256):
    # Convert to jpg
    if jpeg:
        file_path = convert_to_jpg(file_path)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('img_dir', help='Directory of images to compress')
    parser.add_argument('compress_dimension', type=int, help='Max height or width of compressed image')
    parser.add_argument('compress_quality', type=int, help='Quality of compressed image file')
    parser.add_argument('-j', action='store_true', help='Convert images to jpeg')
    parser.add_argument('-v', action='store_true', help='Run in answerer debug mode')
    args = parser.parse_args()

    total_compression = 0
    num_imgs = 0
    for directory, subdirectories, files in os.walk(args.img_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png'):
                    num_imgs += 1
                    percent, filepath, file = compress_me(os.path.join(directory, file),
                            verbose=args.v,
                            jpeg=args.j,
                            quality=args.compress_quality,
                            dimension=args.compress_dimension)
                    total_compression += percent
    print "Average Compression: %d" % (float(total_compression)/num_imgs)
    print "Done"

if __name__ == "__main__":
    main()
