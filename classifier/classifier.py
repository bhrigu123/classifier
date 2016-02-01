import os
import sys
import argparse
import arrow

def move_to(file, from_folder, to_folder):
    from_file = os.path.join(from_folder, file)
    to_file = os.path.join(to_folder, file)

    if os.path.isfile(from_file):
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

def organize_parser():
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

    parser.add_argument('-lc', '--lower_case',action='store_true',
                        help="New directory names are lowercase")

    return parser


def main():
    parser = organize_parser()
    args = parser.parse_args()
    formats = {
        'Music' : ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff'],
        'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts'],
        'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd'],
        'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz'],
        'Documents': ['.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsv', '.xlsx',
            '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
        'Books': ['.mobi', '.epub'],
        'RPMPackages': ['.rpm']
    }

    # else:
    if args.date:
        classify_by_date('DD-MM-YYYY', args.output)
    else:
        if bool(args.specific_folder) ^ bool(args.specific_types):
            print('You must pass in a file type and a folder.')
            sys.exit()

        if args.specific_folder and args.specific_types:
            formats = {args.specific_folder: args.specific_types}

        if args.output is None:
            args.output = os.getcwd()

        if args.lower_case:
            formats = {title.lower():extentions for title, extentions in formats.items()}

        was_moved = classify(formats, args.output)
        if was_moved:
            print('Classified items')
        else:
            print('No items to classify.')

    sys.exit()
