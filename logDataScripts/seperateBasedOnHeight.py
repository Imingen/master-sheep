import json, os, exifread
from datetime import datetime, timedelta

IMAGE_FOLDER = "/home/login/ntnu/data/test-set-jan/data/"

# The path to the images on idun. This makes the .txt files usable there.
INSERT_PATH = "/lustre1/work/johnew/yolov3/sheepData/test-set-jan/data/"
# default height to split images on.
SPLIT_HEIGHT = 50

def attemptToGetHeight(dateAndAltitude, k):
    try:
        value = dateAndAltitude[k]
        return value
    except:
        return False

def readExifTags(path):
    tags = exifread.process_file(open(path, 'rb'))
    key = tags["EXIF DateTimeDigitized"].values
    dt = datetime.strptime(key, '%Y:%m:%d %H:%M:%S')
    return dt

def getListOfPaths(folder, insert_path):
    '''shoud return a list of paths to an images with the relative height included.

    Returns: list of tuples (pathToImage, droneHeight)
    '''
    heights = json.load(open("dateAndAltitude.json"))

    pathWHeight = []
    for image in os.listdir(folder):
        if '.txt' in image:
            continue

        dt = readExifTags(folder+image)
        if not attemptToGetHeight(heights, dt.isoformat()):
            dt += timedelta(seconds=1) 

        print("Image:", image, "Height:", heights[dt.isoformat()])
        pathWHeight.append((insert_path + image, heights[dt.isoformat()]))
    return pathWHeight

def splitBasedOnHeight(pathWHeight, splitHeight):
    high = []; low = []

    for path, height in pathWHeight:
        if float(height) > splitHeight:
            high.append(path + "\n")
        elif float(height) <= splitHeight:
            low.append(path + "\n")
        #TODO: might need to rework everything to include milliseconds
        #       to get more precise measurements.
    return high, low

def writePathsToFile(li, file):
    f = open(file, "a")
    for path in li:
        f.write(path)
    f.close()

def seperateImages(split_height, image_folder, insert_path, imageWHeight=None):
    '''
    Arguments:
        split_height: the height in meters to seperate the list of images on.
        image_folder: a path leading to the image to seperate.
        insert_path: the path added to the outputed files. This is used to add correct image paths on IDUN.
    '''

    #resDict = json.load(open("imagesAndHeights.json"))

    if imageWHeight is None:
        imageWHeight = json.load(open("imagesAndHeights.json"))

    #pathWHeight = getListOfPaths(image_folder, insert_path)
    

    high, low = splitBasedOnHeight(imageWHeight, split_height)

    print("Split on", split_height, "meters", "high:", len(high), "images", "low:", len(low), "images")

    # write to seperate files.
    writePathsToFile(high, "high.txt")
    writePathsToFile(low, "low.txt")



if __name__ == "__main__":
    seperateImages(SPLIT_HEIGHT, IMAGE_FOLDER, INSERT_PATH)

