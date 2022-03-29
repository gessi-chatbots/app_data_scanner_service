import json

import flatdict


def json_to_dict(path):
    """
    Method to load a json file to a Python dict
    """
    with open(path, 'r') as file:
        jsondict = json.load(file)
        return jsondict


def flatten_dict(dictionary_to_normalize):
    flat_dict = flatdict.FlatDict(dictionary_to_normalize, delimiter=".")
    return dict(flat_dict)


def combine_fields(dict1, dict2, same_info_keys):
    combined_dict = {}
    for _tuple in same_info_keys:
        if _tuple[0] not in dict1.keys() or _tuple[1] not in dict2.keys():
            continue
        if dict1[_tuple[0]] == dict2[_tuple[1]]:
            value = dict1[_tuple[0]]
            combined_dict[_tuple[0]] = value
        else:
            value = [dict1[_tuple[0]], dict2[_tuple[1]]]
            combined_dict[_tuple[0]] = value
    return combined_dict


def combine_dicts(dict1, dict2, same_info_keys):
    combined_dict = combine_fields(dict1, dict2, same_info_keys)
    keys1 = []
    keys2 = []

    for i in range(len(same_info_keys)):
        keys1.append(same_info_keys[i][0])
        keys2.append(same_info_keys[i][1])

    for key in dict1.keys():
        if key not in keys1:
            combined_dict[key] = dict1[key]

    for key in dict2.keys():
        if key not in keys2:
            combined_dict[key] = dict2[key]
    return combined_dict


def extract_info(dict1, relevant_keys):
    final_dict = {}
    for key in relevant_keys:
        try:
            final_dict[key] = dict1[key]
        except KeyError:
            raise Exception
    return final_dict
