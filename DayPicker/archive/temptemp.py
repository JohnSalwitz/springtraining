import json
import os
from os import listdir
from os.path import isfile, join

import piexif

mypath = r"C:\\Users\\John\\Dropbox\\Camera Uploads"
json_dict_file = r"jpeg_pix.json"

jpegs = [f for f in listdir(mypath) if isfile(join(mypath, f)) and ".jpg" in f]
movs = [f for f in listdir(mypath) if isfile(join(mypath, f)) and ".mov" in f]

folder_translations = [
    (
        {
            "Model": "Canon EOS DIGITAL REBEL XS"
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\JFS_Canon"
    ),
    (
        {
            "Model": "Canon EOS DIGITAL REBEL XSi"
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\JFS_Canon"
    ),
    (
        {
            "Model": "COOLPIX S3100",
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\CoolPix"
    ),

    (
        {
            "Model": "COOLPIX AW110  ",
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\CoolPix_2"
    ),

    (
        {
            "Model": "iPhone 5s",
            "Make": "Apple"
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\Elizabeth"
    ),

    (
        {
            "Model": "iPhone 4",
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\Elizabeth_IPhone4"
    ),

    (
        {
            "Model": "iPhone 6s",
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\Elizabeth_IPhone6S"
    ),

    (
        {
            "Model": "iPhone 6",
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\Donna_12_18_16"
    ),

    (
        {
            "Model": 'NONE',
        },
        "C:\\Users\\John\\Dropbox\\PHOTOS\\NONE"
    ),

    (
        {
            "Model": 'iPod touch',
        },
        r"C:\\Users\John\Dropbox\PHOTOS\Elizabeth\Old_Photos"
    ),
]


def get_value(dict, key):
    if key in dict["0th"]:
        value = dict["0th"][key]
        value = value.decode("utf-8")
    else:
        value = "NONE"
    return value


def print_key(dict, key):
    value = get_value(dict, key)
    print("{0} == {1}".format(key, value))


def file_matches(info, cryteria):
    for k, v in cryteria.items():
        if not k in info or v != info[k]:
            return False
    return True


def check_and_move(info):
    for ftrans in folder_translations:
        cryteria = ftrans[0]
        if file_matches(info, cryteria):
            source = info["Full_Path"]
            target = os.path.join(ftrans[1], info["File"])
            print(source + " to " + target)
            os.rename(info["Full_Path"], target)

infos = []
limit = 500000
counts = {}

for f in jpegs:
    # print(os.stat(f))
    full_path = os.path.join(mypath, f)
    exif_dict = piexif.load(full_path)


    info = {
        "Full_Path": full_path,
        "File": f,
        "Make": get_value(exif_dict, piexif.ImageIFD.Make),
        "Model": get_value(exif_dict, piexif.ImageIFD.Model),
        "Software": get_value(exif_dict, piexif.ImageIFD.Software),
        "DateTime": get_value(exif_dict, piexif.ImageIFD.DateTime)
    }

    key = (get_value(exif_dict, piexif.ImageIFD.Software), get_value(exif_dict, piexif.ImageIFD.Model))
    if not key in counts:
        counts[key] = 1
    else:
        counts[key] += 1

    infos.append(info)

    check_and_move(info)

    limit -= 1
    if limit == 0:
        break

# for info in infos:
#    print(info)

print()
print()
print("TOTALS...")
for k, v, in counts.items():
    print("{0} = {1}".format(k, v))

print("writing to file")
with open(json_dict_file, 'w') as outfile:
    json.dump(infos, outfile, indent=4)
