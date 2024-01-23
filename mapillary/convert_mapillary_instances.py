
# https://github.com/open-mmlab/mmsegmentation/issues/1572#issuecomment-1125810952

from PIL import Image
import cv2
import numpy as np
import os
import shutil


classes2=['Bird', 'Ground Animal', 'Ambiguous Barrier', 'Concrete Block',
        'Curb', 'Fence', 'Guard Rail', 'Barrier', 'Road Median',
        'Road Side', 'Lane Separator', 'Temporary Barrier', 'Wall',
        'Bike Lane', 'Crosswalk - Plain', 'Curb Cut', 'Driveway',
        'Parking', 'Parking Aisle', 'Pedestrian Area', 'Rail Track',
        'Road', 'Road Shoulder', 'Service Lane', 'Sidewalk',
        'Traffic Island', 'Bridge', 'Building', 'Garage', 'Tunnel',
        'Person', 'Person Group', 'Bicyclist', 'Motorcyclist',
        'Other Rider', 'Lane Marking - Dashed Line',
        'Lane Marking - Straight Line', 'Lane Marking - Zigzag Line',
        'Lane Marking - Ambiguous', 'Lane Marking - Arrow (Left)',
        'Lane Marking - Arrow (Other)', 'Lane Marking - Arrow (Right)',
        'Lane Marking - Arrow (Split Left or Straight)',
        'Lane Marking - Arrow (Split Right or Straight)',
        'Lane Marking - Arrow (Straight)', 'Lane Marking - Crosswalk',
        'Lane Marking - Give Way (Row)',
        'Lane Marking - Give Way (Single)',
        'Lane Marking - Hatched (Chevron)',
        'Lane Marking - Hatched (Diagonal)', 'Lane Marking - Other',
        'Lane Marking - Stop Line', 'Lane Marking - Symbol (Bicycle)',
        'Lane Marking - Symbol (Other)', 'Lane Marking - Text',
        'Lane Marking (only) - Dashed Line',
        'Lane Marking (only) - Crosswalk', 'Lane Marking (only) - Other',
        'Lane Marking (only) - Test', 'Mountain', 'Sand', 'Sky', 'Snow',
        'Terrain', 'Vegetation', 'Water', 'Banner', 'Bench', 'Bike Rack',
        'Catch Basin', 'CCTV Camera', 'Fire Hydrant', 'Junction Box',
        'Mailbox', 'Manhole', 'Parking Meter', 'Phone Booth', 'Pothole',
        'Signage - Advertisement', 'Signage - Ambiguous', 'Signage - Back',
        'Signage - Information', 'Signage - Other', 'Signage - Store',
        'Street Light', 'Pole', 'Pole Group', 'Traffic Sign Frame',
        'Utility Pole', 'Traffic Cone', 'Traffic Light - General (Single)',
        'Traffic Light - Pedestrians', 'Traffic Light - General (Upright)',
        'Traffic Light - General (Horizontal)', 'Traffic Light - Cyclists',
        'Traffic Light - Other', 'Traffic Sign - Ambiguous',
        'Traffic Sign (Back)', 'Traffic Sign - Direction (Back)',
        'Traffic Sign - Direction (Front)', 'Traffic Sign (Front)',
        'Traffic Sign - Parking', 'Traffic Sign - Temporary (Back)',
        'Traffic Sign - Temporary (Front)', 'Trash Can', 'Bicycle', 'Boat',
        'Bus', 'Car', 'Caravan', 'Motorcycle', 'On Rails', 'Other Vehicle',
        'Trailer', 'Truck', 'Vehicle Group', 'Wheeled Slow', 'Water Valve',
        'Car Mount', 'Dynamic', 'Ego Vehicle', 'Ground', 'Static',
        'Unlabeled']

classes1=['Bird', 'Ground Animal', 'Curb', 'Fence', 'Guard Rail',
                 'Barrier', 'Wall', 'Bike Lane', 'Crosswalk - Plain',
                 'Curb Cut', 'Parking', 'Pedestrian Area', 'Rail Track',
                 'Road', 'Service Lane', 'Sidewalk', 'Bridge', 'Building',
                 'Tunnel', 'Person', 'Bicyclist', 'Motorcyclist',
                 'Other Rider', 'Lane Marking - Crosswalk',
                 'Lane Marking - General', 'Mountain', 'Sand', 'Sky', 'Snow',
                 'Terrain', 'Vegetation', 'Water', 'Banner', 'Bench',
                 'Bike Rack', 'Billboard', 'Catch Basin', 'CCTV Camera',
                 'Fire Hydrant', 'Junction Box', 'Mailbox', 'Manhole',
                 'Phone Booth', 'Pothole', 'Street Light', 'Pole',
                 'Traffic Sign Frame', 'Utility Pole', 'Traffic Light',
                 'Traffic Sign (Back)', 'Traffic Sign (Front)', 'Trash Can',
                 'Bicycle', 'Boat', 'Bus', 'Car', 'Caravan', 'Motorcycle',
                 'On Rails', 'Other Vehicle', 'Trailer', 'Truck',
                 'Wheeled Slow', 'Car Mount', 'Ego Vehicle', 'Unlabeled']

road = ['Road', 'Road Shoulder', 'Service Lane', 'Parking', 'Parking Aisle', 'Rail Track', 'Bike Lane',
        'Lane Marking - Dashed Line',
        'Lane Marking - Straight Line', 'Lane Marking - Zigzag Line',
        'Lane Marking - Ambiguous', 'Lane Marking - Arrow (Left)',
        'Lane Marking - Arrow (Other)', 'Lane Marking - Arrow (Right)',
        'Lane Marking - Arrow (Split Left or Straight)',
        'Lane Marking - Arrow (Split Right or Straight)',
        'Lane Marking - Arrow (Straight)',
        'Lane Marking - Give Way (Row)',
        'Lane Marking - Give Way (Single)',
        'Lane Marking - Hatched (Chevron)',
        'Lane Marking - Hatched (Diagonal)', 'Lane Marking - Other',
        'Lane Marking - Stop Line', 'Lane Marking - Symbol (Bicycle)',
        'Lane Marking - Symbol (Other)', 'Lane Marking - Text',
        'Lane Marking (only) - Dashed Line',
        'Lane Marking (only) - Other',
        'Lane Marking (only) - Test',
        'Driveway']
plain = ['Crosswalk - Plain']
zebra = ['Lane Marking - Crosswalk', 'Lane Marking (only) - Crosswalk']
sidewalk = ['Sidewalk', 'Pedestrian Area']
curb = ['Curb']
curbcut = ['Curb Cut']
covering = ['Catch Basin', 'Manhole']
void = ['Ground', 'Pothole', 'Traffic Island']
terrain = ['Terrain']

everything = [terrain, road, curb, curbcut, sidewalk, plain, zebra, covering, void]
labels = [1, 2, 3, 4, 5, 6, 7, 8, 255]

palette2 = {}
for i, classlist in enumerate(everything):
    for name in classlist:
        palette2[classes2.index(name)] = labels[i]

palette1 = {}
palette1[classes1.index('Sidewalk')] = 5


def color_to_labels(filepath, filepath2):
    result = cv2.imread(filepath, 0)
    arr_2d = np.zeros((result.shape[0], result.shape[1]), dtype=np.uint8)
    for c, i in palette2.items():
        arr_2d[result == c] = i

    result = cv2.imread(filepath2, 0)
    for c, i in palette1.items():
        arr_2d[result == c] = i

    return arr_2d

labeldir = 'training/v1.2/instances'
labeldir2 = 'training/v2.0/instances'
converteddir = 'training/converted_labels'
for subdir, dirs, files in os.walk(labeldir2):
    for file in files:
        filepath = os.path.join(subdir, file)
        filepath2 = os.path.join(labeldir, file)
        arr_2d = color_to_labels(filepath, filepath2)
        im = Image.fromarray(arr_2d.astype(np.uint8))
        im.save(os.path.join(converteddir, file))

labeldir = 'validation/v1.2/instances'
labeldir2 = 'validation/v2.0/instances'
converteddir = 'validation/converted_labels'
for subdir, dirs, files in os.walk(labeldir2):
    for file in files:
        filepath = os.path.join(subdir, file)
        filepath2 = os.path.join(labeldir, file)
        arr_2d = color_to_labels(filepath, filepath2)
        im = Image.fromarray(arr_2d.astype(np.uint8))
        im.save(os.path.join(converteddir, file))