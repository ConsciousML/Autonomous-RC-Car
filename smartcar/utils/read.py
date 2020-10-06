import json

"""

This file contains all functions of the project that read values
in files.

"""


def read_json_label(path):
    """Returns the label values of a json label file
    
    Args:
        paths: A string for the json label path

    Returns:
        A numpy array containing all the labels in the input file.

    Example:
        The input should be of the form:
        {"label1": 0.5444, "label2": 0.5444 ...}
    """
    with open(path) as f:
        label_dict = json.load(f)
    labels = np.zeros(len(label_dict))
    dict_keys = label_dict.keys()
    idx = 0
    for key in label_dict.keys():
        labels[idx] = label_dict[key]
        idx += 1
    return labels