#!/usr/bin/env python
import argparse
import arrow
import os
import six
import sys
import json
from six.moves import getcwd

"""
All format lists were taken from wikipedia, not all of them were added due to extensions
not being exclusive to one format such as webm, or raw
Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
"""


def moveto(file, from_folder, to_folder):
    from_file = os.path.join(from_folder, file)
    to_file = os.path.join(to_folder, file)

    # to move only files, not folders
    if os.path.isfile(from_file):
        if not os.path.exists(to_folder):
            os.makedirs(to_folder)
        os.rename(from_file, to_file)


def classify(formats, output):
    print("Scanning Files")
    directory = getcwd()
    obj = []

    for file in [x for x in os.listdir(directory) if not x.startswith('.')]:
        filename, file_ext = os.path.splitext(file)
        file_ext = file_ext.lower()

        for folder, ext_list in list(formats.items()):
            folder = os.path.join(output, folder)

            if file_ext in ext_list:
                try:
                    moveto(file, directory, folder)
                    obj.append({"file": file, "directory": directory, "folder": folder})

                except Exception as e:
                    print('Cannot move file - {} - {}'.format(file, str(e)))
    # record info to json
    dump_json(0, obj)
    print("Done!")


def classify_by_date(date_format, output_dir):
    print("Scanning Files")
    directory = getcwd()
    obj = []
    files = [x for x in os.listdir(directory) if not x.startswith('.')]
    creation_dates = map(lambda x: (x, arrow.get(os.path.getctime(x))), files)

    for file, creation_date in creation_dates:
        folder = creation_date.format(date_format)
        moveto(file, directory, folder)
        obj.append({"file": file, "directory": directory, "folder": folder})
    # record info to json
    dump_json(0, obj)
    print("Done!")


def classify_redo(output):
    print("Scanning Files")
    obj = load_json()
    status, items = obj['status'], obj['obj_json']
    # check repeat
    if int(status) == -1:
        print("Repeat redo")
        return
    else:
        dump_json(-1, items)

    for item in items:
        file, directory, folder = item['file'], item['directory'], item['folder']
        dir_der = os.path.join(directory, folder)
        try:
            moveto(file, dir_der, directory)
        except Exception as e:
            print("Redo Files - {} - {}".format(file, str(e)))
        # remove the (directory+folder)
        if len([x for x in os.listdir(dir_der) if not x.startswith('.')]) == 0:
            os.rmdir(dir_der)

    # remove --output
    if len([x for x in os.listdir(output) if not x.startswith('.')]) == 0:
        os.removedirs(output)
    print("Done!")

def dump_json(status, obj):
    obj_json = {"status": status, "obj_json": obj}
    with open(".redo.json", "wt") as fp:
        json.dump(obj_json, fp, ensure_ascii=False, indent=4, sort_keys=True)


def load_json():
    with open(".redo.json", "rt") as fp:
        obj = json.load(fp)
    return obj


def _format_text_arg(arg):
    if not isinstance(arg, six.text_type):
        arg = arg.decode('utf-8')
    return arg


def _format_arg(arg):
    if isinstance(arg, six.string_types):
        arg = _format_text_arg(arg)
    return arg


def main():
    description = "Organize files in your directory instantly,by classifying them into different folders"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-st", "--specific-types", type=str, nargs='+',
                        help="Move all file extensions, given in the args list, in the current directory into the Specific Folder")

    parser.add_argument("-sf", "--specific-folder", type=str,
                        help="Folder to move Specific File Type")

    parser.add_argument("-o", "--output", type=str,
                        help="Main directory to put organized folders")

    parser.add_argument("-dt", "--date", action='store_true',
                        help="Organize files by creation date")
    parser.add_argument("-rd", "--redo", action='store_true',
                        help="Redo the last action")

    args = parser.parse_args()

    formats = {
        'Music': ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff', '.wav'],
        'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts'],
        'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd'],
        'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz', '.xz'],
        'Documents': ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsv', '.xlsx',
                      '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
        'Books': ['.mobi', '.epub', '.chm'],
        'DEBPackages': ['.deb'],
        'RPMPackages': ['.rpm']
    }

    if bool(args.specific_folder) ^ bool(args.specific_types):
        print(
            'Specific Folder and Specific Types need to be specified together')
        sys.exit()

    if args.specific_folder and args.specific_types:
        specific_folder = _format_arg(args.specific_folder)
        formats = {specific_folder: args.specific_types}

    if args.output is None:
        output = getcwd()
    else:
        output = _format_arg(args.output)

    if args.date:
        classify_by_date('DD-MM-YYYY', output)
    elif args.redo:
        classify_redo(output)
    else:
        classify(formats, output)

    sys.exit()
