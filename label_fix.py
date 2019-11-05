import os, json
import pandas as pd



CSV_PATH = ""
SAVE_PATH = ""

IMG_WIDTH = 1024
IMG_HEIGHT = 1024
FILE_EXT = '.txt'


    
def make_labels(dataframe, skipvalue="Skip"):
    """
    Marius trying to make OP Google-type docstring cuz why the fuck not JIMBOOOOO

    Args:
        dataframe = pandas dataframe
        skipvalue = (optional) value that indicates if a row(picture) has no label
    
    Returns:
        My foot up your ass
    """

    for index, row in dataframe.iterrows():
        if row["Label"] == skipvalue:
            continue
        else:
            label_dict = json.loads(row["Label"]) # Using json module to de-serialize the string in this single DF-cell
            new_coords = iter_label_values(label_dict) # make new yolo coords,
            write_label_file(new_coords, row["External ID"]) # writes new yolo coords to files
            


def iter_label_values(labels):
    yolo_coords = []
    for key, value in labels.items():
        for elem in labels[key]:
            label_coord = calc_yolo_coords(elem["geometry"])
            yolo_coords.append(label_coord)
    return yolo_coords


def calc_yolo_coords(geometry):
    """Calculates the yolo-coordinates. Uses min and max cuz there was no 
    order in the csv file. i.e sometimes index 0 was biggest other time index 2 was biggest. 

    Args:
        geometry: A list of dicts. Where each dict is x: and y: values for a corner of bbox
    
    Returns:
        A list of yolo-coordinates, relative to image height/width
    """
    x0 = min([l['x'] for l in geometry])
    x1 = max([l['x'] for l in geometry])
    y0 = min([l['y'] for l in geometry])
    y1 = max([l['y'] for l in geometry])

    x_center = (x0 + x1) / 2
    y_center = (y0 + y1) / 2
    width = x1 - x0
    height = y1 - y0

    return [x_center/1024, y_center/1024, width/1024, height/1024]

def write_label_file(yolo_coords, label_ID):
    filename = label_ID[:-4] + FILE_EXT # removes .jpg extension
    filename = "Split-farge-" + filename 
    y = yolo_coords
    
    for i, bbox in enumerate(y):
        bbox.insert(0, 0)
        x = ' '.join(str(e) for e in bbox)
        y[i] = x

    with open("/home/marius/ntnu/master/Split-farge/" + filename, "w") as f:
        for elem in y:
            f.write(elem)
            f.write("\n")


if __name__ == "__main__":
    path_to_csv = '/home/marius/ntnu/master/scripts/splitfarge.csv'
    content = pd.read_csv(path_to_csv, usecols=["External ID", "Label"])
    make_labels(content)






