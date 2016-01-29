import argparse
import os

global formats
from .config import formats
from .classifier import classify


def main():
    description =   "Organize files in your directory instantly, "
    description +=  "by classifying them into different folders"
    parser = argparse.ArgumentParser(description = description)

    parser.add_argument("-st", "--specific-types", type=str, nargs='+',
                        help="Move all file extensions, given in the args list, in the current directory into the Specific Folder")

    parser.add_argument("-sf", "--specific-folder", type=str,
                        help="Folder to move Specific File Type")

    parser.add_argument("-o","--output", type=str,
                        help="Main directory to put organized folders")

    args = parser.parse_args()

    if ((args.specific_folder is None) != (args.specific_types is None)):
        print('Specific Folder and Specific Types should be combined')
        sys.exit()

    if ((not (args.specific_folder is None)) and (not (args.specific_types is None))):
        formats = {args.specific_folder : args.specific_types}

    if (args.output is None):
        args.output = os.getcwd()

    classify(formats, args.output)
