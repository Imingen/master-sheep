import json, os, exifread
from datetime import datetime, timedelta

IMAGE_FOLDER = "/home/login/ntnu/data/test-set-jan/data/"
SPLIT_HEIGHT = 50
INSERT_PATH = "/lustre1/work/johnew/yolov3/sheepData/test-set-jan/data/"

def splitBasedOnHeight(pathWHeight, splitHeight):
    high = []; low = []

    for path, height in pathWHeight:
        if float(height) > splitHeight:
            high.append(path + "\n")
        elif float(height) <= splitHeight:
            low.append(path + "\n")
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

    if imageWHeight is None:
        imageWHeight = json.load(open("imagesAndHeights.json"))


    high, low = splitBasedOnHeight(imageWHeight, split_height)

    print("Split on", split_height, "meters", "high:", len(high), "images", "low:", len(low), "images")

    # write to seperate files.
    writePathsToFile(high, "high.txt")
    writePathsToFile(low, "low.txt")


if __name__ == "__main__":
    seperateImages(SPLIT_HEIGHT, IMAGE_FOLDER, INSERT_PATH) # not even sure if this works anymore.

