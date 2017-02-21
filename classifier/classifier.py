#!/usr/bin/env python
import argparse
import arrow
import os
import six
import sys
import yaml

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


def classify(formats, output, directory):
    print("Scanning Files")

    for file in os.listdir(directory):
        filename, file_ext = os.path.splitext(file)
        file_ext = file_ext.lower()

        for folder, ext_list in list(formats.items()):
            folder = os.path.join(output, folder)

            if file_ext in ext_list:
                try:
                    moveto(file, directory, folder)
                except Exception as e:
                    print('Cannot move file - {} - {}'.format(file, str(e)))

    print("Done!")


def classify_by_date(date_format, output, directory):
    print("Scanning Files")

    files = [x for x in os.listdir(directory) if not x.startswith('.')]
    creation_dates = map(lambda x: (x, arrow.get(os.path.getctime(os.path.join(directory, x)))), files)

    for file, creation_date in creation_dates:
        folder = creation_date.format(date_format)
        folder = os.path.join(output, folder)
        moveto(file, directory, folder)

    print("Done!")


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

    parser.add_argument("-d", "--directory", type=str,
                        help="The directory whose files to classify")

    parser.add_argument("-dt", "--date", action='store_true',
                        help="Organize files by creation date")

    parser.add_argument("-c", "--config", type=str,
                        help="Config file")

    args = parser.parse_args()

    if args.config:
        conf_file_name = os.path.expanduser(args.config)
    else:
        conf_file_name = os.getenv("HOME") + "/.config/.classify.conf"

    if os.path.exists(conf_file_name):
        with open(conf_file_name, "r") as conf_file:
            formats = yaml.load(conf_file)
    else:
        formats = {
            'Music'	: ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff', '.wav', '.amr'],
            'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts', '.webm', '.vob', '.wmv'],
            'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd', '.tiff'],
            'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz', '.xz', '.iso', '.cpio'],
            'Documents': ['.txt', '.pdf', '.doc', '.docx','.odf', '.xls', '.xlsv', '.xlsx',
                              '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
            'Books': ['.mobi', '.epub', '.chm'],
            'DEBPackages': ['.deb'],
            'Programs': ['.exe', '.msi'],
            'RPMPackages': ['.rpm']
        }
        with open(conf_file_name, 'w') as conf_file:
            yaml.safe_dump(formats, conf_file)

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

    if args.directory is None:
        directory = getcwd()
    else:
        directory = _format_arg(args.directory)
        if args.output is None:
            ''' if -d arg given without the -o arg, keeping the files of -d
            in the -d path only after classifying '''
            output = directory

    if args.date:
        classify_by_date('DD-MM-YYYY', output, directory)
    else:
        classify(formats, output, directory)

    sys.exit()
