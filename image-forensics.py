from PIL import Image
from PIL.ExifTags import TAGS
import argparse
import glob
import sys
import os

if sys.version_info.major==2:
    input = raw_input

def coordinates(ImageObject):
    """This function takes in a PIL Image Object and returns a longitude and latitude. For example: xlong,xlat = coordinates(imageobject) """
    info = ImageObject._getexif()
    if not info or not info.get(34853):
        return 0,0
    # 34853: contains 'GPSInfo'
    # info[34853][1] = 'N'
    # Latitude at info[3.4853][2] =  ((49, 1), (4363, 1000), (0, 1))
    # info[34853][3] = 'W'
    # Longitude at info[34853][4] =  ((123, 1), (2103, 1000), (0, 1))
    latDegrees = info[34853][2][0][0]/float(info[34853][2][0][1]) 
    latMinutes = info[34853][2][1][0]/float(info[34853][2][1][1])/60 
    latSeconds = info[34853][2][2][0]/float(info[34853][2][2][1])/3600 
    lonDegrees = info[34853][4][0][0]/float(info[34853][4][0][1]) 
    lonMinutes = info[34853][4][1][0]/float(info[34853][4][1][1])/60 
    lonSeconds = info[34853][4][2][0]/float(info[34853][4][2][1])/3600 
    # correct the lat/lon based on N/E/W/S 
    latitude = latDegrees + latMinutes + latSeconds
    if info[34853][1] == 'S':
        latitude*= -1
    longitude = lonDegrees + lonMinutes + lonSeconds 
    if info[34853][3] == 'W':
        longitude*=-1
    return longitude,latitude


def print_exif(ImageObject):
    """The print_exif function will take in a PIL ImageObject and print all of the EXIF data along with the associated EXIF Tag"""
    exifdict=ImageObject._getexif()
    if exifdict:
       for name,data in list(exifdict.items()):
           tagname="unknown-tag"
           if name in TAGS:
               tagname=TAGS[name]
           print("TAG:%s (%s) is assigned %s" % (name,tagname,data)) 
    return


parser=argparse.ArgumentParser()
parser.add_argument('-d','--display',action='store_true',required=False,help='Display the image')
parser.add_argument('-m','--maps',action='store_true',required=False,help='Print google maps links')
parser.add_argument('-e','--exif',action='store_true',required=False,help='Display the exif data')
parser.add_argument('-p','--pause',action='store_true',required=False,help='Pause after each image')
parser.add_argument('image_directory', help='A file path containing images to process')
args=parser.parse_args()

if not args.display and not args.maps and not args.exif :
    print("Nothing to do.  Choose one or more actions.")
    parser.print_help()
    sys.exit(1)

if not args.image_directory.endswith("/"):
    args.image_directory+="/"

if not os.path.exists(args.image_directory):
    print("Directory doesn't exist")
    sys.exit(2)

listoffiles = glob.glob(args.image_directory + "*.jpg")
if len(listoffiles)==0:
   print("No Matching files found matching %s*.jpg" % (args.image_directory))
   sys.exit(3)

for file in listoffiles:
    print("[*] Processing file %s " % (file))
    try:
        imageobject = Image.open(file)
    except Exception as e:
        print("An exception occured displaying the image." + str(e))
        continue
    if args.exif:
        #Print the EXIF data from the image
        print_exif(imageobject)
    if args.maps:
        #Print a link to google maps of the coordinates in the image
        lon, lat = coordinates(imageobject)
        if lon and lat:
            print("https://maps.google.com/maps?q=%.9f,%.9f&z=15" % (lat, lon))
    if args.display: 
        #Resize the image to 200x200 and display it
        newimage = imageobject.resize((200, 200), Image.ANTIALIAS)
        newimage.show()
    if args.pause:
        x = input("Press enter to continue")

