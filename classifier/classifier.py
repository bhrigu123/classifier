#!/usr/bin/env python
import os
import sys
import argparse
import arrow

"""
All format lists were taken from wikipedia, not all of them were added due to extensions
not being exclusive to one format such as webm, or raw
Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
"""


def move_to(file, from_folder, to_folder):
    from_file = os.path.join(from_folder, file)
    to_file = os.path.join(to_folder, file)

    #to move only files, not folders
    if(os.path.isfile(from_file)):
        if not os.path.exists(to_folder):
            os.makedirs(to_folder)
            
        os.rename(from_file, to_file)

def classify(formats, output):
    moved_any = False
    directory = os.getcwd()
    for a_file in os.listdir(directory):
        filename, file_ext = os.path.splitext(a_file)
        file_ext = file_ext.lower()

        for folder, ext_list in list(formats.items()):
            folder = os.path.join(output, folder)

            if file_ext in ext_list:
                move_to(a_file, directory, folder)
                moved_any = True
    return moved_any

def classify_by_date(date_format, output_dir):
    directory = os.getcwd()
    files = os.listdir(directory)
    creation_dates = map(lambda x: (x, arrow.get(os.path.getctime(x))), files)

    for file, creation_date in creation_dates:
        folder = creation_date.format(date_format)
        move_to(file, directory, folder)

def main():
    description = "Organize files in your directory instantly,by classifying them into different folders"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-st", "--specific_types", type=str, nargs='+',
                        help="Move all file extensions, given in the args list, in the current directory into the Specific Folder")

    parser.add_argument("-sf", "--specific_folder", type=str,
                        help="Folder to move Specific File Type")

    parser.add_argument("-o", "--output", type=str,
                        help="Main directory to put organized folders")

    parser.add_argument("-dt", "--date", action='store_true',
                        help="Organize files by creation date")

    args = parser.parse_args()

    formats = {
        'Music'	: ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff'],
        'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts'],
        'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd'],
        'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz'],
        'Documents': ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsv', '.xlsx',
        '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
        'Books': ['.mobi', '.epub'],
        'RPMPackages': ['.rpm']
    }

    if not len(sys.argv) > 1:
        parser.print_help()
    else:        
        if bool(args.specific_folder) ^ bool(args.specific_types):
            print('You must pass in a file type and a folder.')
            sys.exit()

        if args.specific_folder and args.specific_types:
            formats = {args.specific_folder: args.specific_types}

        if args.output is None:
            args.output = os.getcwd()

        if args.date:
            classify_by_date('DD-MM-YYYY', args.output)
        else:
            was_moved = classify(formats, args.output)
            if was_moved:
                print('Moved {0} files into /{1}'.format(
                    args.specific_types[0], args.specific_folder))
            else:
                print('No files ending with {0} are in the current directory'.format(
                    args.specific_types[0]))

    sys.exit()
