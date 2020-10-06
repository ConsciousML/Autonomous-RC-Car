import os

"""

This python file contains function that gather, move or modify files.

"""

def get_data_paths(dir):
    """Returns the images and labels from a directory"""
    image_plist = []
    label_plist = []
    for root, _, files in os.walk(dir):
        for f in files:
            if not f.endswith('.jpg'):
                continue
            image_path = os.path.join(root, f)
            label_path = image_path[:-4] + '.json'
            if not os.path.exists(label_path):
                continue
            image_plist.append(image_path)
            label_plist.append(label_path)
    return image_plist, label_plist
