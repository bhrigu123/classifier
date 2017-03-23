#!/usr/bin/env python

""" Classifier

    ----------------Authors----------------
    Bhrigu Srivastava <captain.bhrigu@gmail.com>
    ----------------Licence----------------
    The MIT License [https://opensource.org/licenses/MIT]
    Copyright (c) 2015 Bhrigu Srivastava http://bhrigu123.github.io

"""

import argparse
import arrow
import os
import sys

VERSION = 'Classifier 1.99dev'


class Classifier:
    """
    All format lists were taken from wikipedia, not all of them were added due to extensions
    not being exclusive to one format such as webm, or raw
    Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
    Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
    Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
    Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
    """

    def __init__(self):
        self.description = "Organize files in your directory instantly,by classifying them into different folders"
        self.parser = argparse.ArgumentParser(description=self.description)

        self.parser.add_argument("-v", "--version", action='store_true',
                                 help="show version, filename and exit")

        self.parser.add_argument("-st", "--specific-types", type=str, nargs='+',
                                 help="Move all file extensions, given in the args list, " +
                                      "in the current directory into the Specific Folder")

        self.parser.add_argument("-sf", "--specific-folder", type=str,
                                 help="Folder to move Specific File Type")

        self.parser.add_argument("-o", "--output", type=str,
                                 help="Main directory to put organized folders")

        self.parser.add_argument("-d", "--directory", type=str,
                                 help="The directory whose files to classify")

        self.parser.add_argument("-dt", "--date", action='store_true',
                                 help="Organize files by creation date")

        self.args = self.parser.parse_args()

        self.formats = {
            'Music': ['.mp3', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.aiff', '.wav', '.amr'],
            'Videos': ['.flv', '.ogv', '.avi', '.mp4', '.mpg', '.mpeg', '.3gp', '.mkv', '.ts', '.webm', '.vob', '.wmv'],
            'Pictures': ['.png', '.jpeg', '.gif', '.jpg', '.bmp', '.svg', '.webp', '.psd', '.tiff'],
            'Archives': ['.rar', '.zip', '.7z', '.gz', '.bz2', '.tar', '.dmg', '.tgz', '.xz', '.iso', '.cpio'],
            'Documents': ['.txt', '.pdf', '.doc', '.docx', '.odf', '.xls', '.xlsv', '.xlsx',
                          '.ppt', '.pptx', '.ppsx', '.odp', '.odt', '.ods', '.md', '.json', '.csv'],
            'Books': ['.mobi', '.epub', '.chm'],
            'DEBPackages': ['.deb'],
            'Programs': ['.exe', '.msi'],
            'RPMPackages': ['.rpm']
        }
        self.main()

    def moveto(self, filename, from_folder, to_folder):
        from_file = os.path.join(from_folder, filename)
        to_file = os.path.join(to_folder, filename)

        # to move only files, not folders
        if os.path.isfile(from_file):
            if not os.path.exists(to_folder):
                os.makedirs(to_folder)
            os.rename(from_file, to_file)
        return

    def classify(self, formats, output, directory):
        print("Scanning Files")

        for file in os.listdir(directory):
            # set up a config per folder
            if not file == '.classify.conf':
                filename, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower()

                for folder, ext_list in list(formats.items()):
                    folder = os.path.join(output, folder)

                    if file_ext in ext_list:
                        try:
                            self.moveto(file, directory, folder)
                        except Exception as e:
                            print('Cannot move file - {} - {}'.format(file, str(e)))

        print("Done!")
        return

    def classify_by_date(self, date_format, output, directory):
        print("Scanning Files")

        files = [x for x in os.listdir(directory) if not x.startswith('.')]
        creation_dates = map(lambda x: (x, arrow.get(os.path.getctime(os.path.join(directory, x)))), files)
        print(creation_dates)

        for file, creation_date in creation_dates:
            folder = creation_date.format(date_format)
            folder = os.path.join(output, folder)
            self.moveto(file, directory, folder)

        print("Done!")
        return

    def _format_text_arg(self, arg):
        if not isinstance(arg, str):
            arg = arg.decode('utf-8')
        return arg

    def _format_arg(self, arg):
        if isinstance(arg, str):
            arg = self._format_text_arg(arg)
        return arg

    def main(self):
        if self.args.version:
            print(VERSION + '\n' + os.path.realpath(__file__))
            return False
        if bool(self.args.specific_folder) ^ bool(self.args.specific_types):
            print(
                'Specific Folder and Specific Types need to be specified together')
            sys.exit()

        if self.args.specific_folder and self.args.specific_types:
            specific_folder = self._format_arg(self.args.specific_folder)
            self.formats = {specific_folder: self.args.specific_types}

        if self.args.output is None:
            output = os.getcwd()
        else:
            output = self._format_arg(self.args.output)

        if self.args.directory is None:
            directory = os.getcwd()
        else:
            directory = self._format_arg(self.args.directory)
            if self.args.output is None:
                ''' if -d arg given without the -o arg, keeping the files of -d
                in the -d path only after classifying '''
                output = directory

        if self.args.date:
            self.classify_by_date('YYYY-MM-DD', output, directory)
        else:
            self.classify(self.formats, output, directory)

        return True


Classifier()
