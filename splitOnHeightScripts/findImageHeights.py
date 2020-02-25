import csv, os, exifread, json, collections, bisect

from datetime import datetime, timedelta
from seperateBasedOnHeight import seperateImages

PATH_TO_LOGFILES = "/home/login/ntnu/data/loggdata/"
PATH_TO_EXIF_IMAGE_FOLDER = "/home/login/ntnu/data/allThermal-2/compiled/"
INSERT_PATH = "/lustre1/work/johnew/yolov3/sheepData/test-set-jan/data/"
LOG_TO_IMAGE_MAX_DELTA_TIME = 3     # how many seconds the log entry can be different from the image.
SPLIT_HEIGHT = 50


def csvRead(file):
    '''reads the given csv file and extracts relative height and time.

    file: string used to load csv file.
    Returns: a list of tuples with the date and drones relative height at that date.
    '''
    # logs from 1900s are illegal
    file_t0 = datetime.strptime("20"+file[:17], '%Y-%m-%d-%H-%M-%S')

    dateAndAltitude = []
    with open(PATH_TO_LOGFILES + file) as csv_file:

        line_count = 0
        for row in csv.reader(csv_file, delimiter=","):
            if line_count == 0:
                line_count += 1
                continue
            time = file_t0 + timedelta(seconds= float(row[1]))
            dateAndAltitude.append((time, row[38]))

    # sort on datetime.
    dateAndAltitude = sorted(dateAndAltitude, key=lambda x: x[0])
    dateDict = collections.OrderedDict()
    dateDict = {key.isoformat(): value for (key, value) in dateAndAltitude}
 
    return dateDict
            
def readExif(folder):
    '''reads all the .jpg or .JPG images in the given folder 
        and extracts the exif information.
    
    Returns: a list of tuples (the image name, tine it was taken)
    '''
    imagesWithDate = []
    for image in os.listdir(folder):
        if ".jpg" not in image and ".JPG" not in image:
            continue # skip 
        
        with open(folder+image, 'rb') as f:
            tags = exifread.process_file(f, details=False)

        if "EXIF DateTimeDigitized" not in tags:
            print("No EXIF data on image:", image)
            continue
        
        imagesWithDate.append((image, tags["EXIF DateTimeDigitized"]))
    return imagesWithDate

def toDateTime(string):
    return datetime.strptime(str(string), "%Y:%m:%d %H:%M:%S")

def getDateAndAltitudes():
    '''reads all the drone logs and compiles it into a dictionary'''
    dateAndAltitude = collections.OrderedDict()
    for file in os.listdir(PATH_TO_LOGFILES):
        dateAndAltitude = dict(dateAndAltitude, **csvRead(file))
        print("loaded:", len(dateAndAltitude), "out of 57038")
    return dateAndAltitude

def compileData(imagesWithDate, dateAndAltitude):
    resList = []; i = 1
    test = [k for k, v in dateAndAltitude.items()]
    test.sort()
    print(test[0])

    for image, date in imagesWithDate:
        print("Image ", str(i), "of", len(imagesWithDate), "-----------------------------------------------------------------")
        i += 1

        matchKey = toDateTime(date.values).isoformat()

        compare = lambda key: abs(datetime.fromisoformat(key)-datetime.fromisoformat(matchKey))
        key = min(dateAndAltitude.keys(), key=compare)
        logImage_dt = abs(datetime.fromisoformat(key) - datetime.fromisoformat(matchKey))
        
        if logImage_dt >= timedelta(seconds=LOG_TO_IMAGE_MAX_DELTA_TIME):
            print("Log file and image are off by:", str( abs( datetime.fromisoformat(key) - datetime.fromisoformat(matchKey)))
                  , "image date:", matchKey, " Found date:", key)
            #print(list(dateAndAltitude)[(keyIndex-2):(keyIndex+2)])
            continue    # DONT append this entry.
        if dateAndAltitude[key] == "":
            print("Empty so skipped"); continue
        
        print(image, "\theight:", round(float(dateAndAltitude[key]), 3), "   \t| dt:", logImage_dt)
        resList.append((INSERT_PATH + image, dateAndAltitude[key]))
    return resList

def main():
    '''This script should create a json file with image name 
    '''
    if not os.path.isfile("dateAndAltitude.json"):
        json.dump(getDateAndAltitudes(), open("dateAndAltitude.json", 'w'), indent=2)
    
    dateAndAltitude = collections.OrderedDict()
    dateAndAltitude = json.load(open("dateAndAltitude.json"))
    # get EXIF data
    imagesWithDate = readExif(PATH_TO_EXIF_IMAGE_FOLDER)

    if not os.path.isfile("imagesAndHeights.json"):
        json.dump(compileData(imagesWithDate, dateAndAltitude), open("imagesAndHeights.json", 'w'), indent=2)
    
    imagesWHeight = json.load(open("imagesAndHeights.json"))

    seperateImages(SPLIT_HEIGHT, PATH_TO_EXIF_IMAGE_FOLDER, INSERT_PATH, imageWHeight=imagesWHeight)
    

if __name__ == "__main__":
    main()