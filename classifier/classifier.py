#!/usr/bin/env python

""" Classifier
    ----------------Contributors----------------
    https://github.com/bhrigu123/classifier/graphs/contributors
    ----------------Maintainer----------------
    Bhrigu Srivastava <captain.bhrigu@gmail.com>
    ----------------License----------------
    The MIT License [https://opensource.org/licenses/MIT]
    Copyright (c) 2015 Bhrigu Srivastava http://bhrigu.me

"""

import argparse
import arrow
import os
import subprocess
import sys


VERSION = 'Classifier 2.0'
DIRCONFFILE = '.classifier.conf'
PLATFORM = sys.platform
OS = os.name

if PLATFORM == 'darwin':
    CONFIG = os.path.join(os.path.expanduser('~'), '.classifier-master.conf')
elif PLATFORM == 'win32' or OS == 'nt':
    CONFIG = os.path.join(os.getenv('userprofile'), 'classifier-master.conf')
elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
    CONFIG = os.path.join(os.getenv('HOME'), '.classifier-master.conf')
else:
    CONFIG = os.path.join(os.getcwd(), '.classifier-master.conf')


def main():
    Classifier()


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

        self.parser.add_argument("-et", "--edittypes", action='store_true',
                                 help="Edit the list of types and formats")

        self.parser.add_argument("-t", "--types", action='store_true',
                                 help="Show the current list of types and formats")

        self.parser.add_argument("-rst", "--reset", action='store_true',
                                 help="Reset the default Config file")
        
        """
        self.parser.add_argument("-r", "--recursive", action='store_true',
                                 help="Recursively search your source directory. " +
                                 "WARNING: Ensure you use the correct path as this " +
                                 "WILL move all files from your selected types.")
        """        

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

        self.parser.add_argument("-df", "--dateformat", type=str,
                                 help="set the date format using YYYY, MM or DD")

        self.args = self.parser.parse_args()
        self.dateformat = 'YYYY-MM-DD'
        self.formats = {}
        self.dirconf = None
        self.checkconfig()
        self.run()

    def create_default_config(self):
        with open(CONFIG, "w") as conffile:
            conffile.write("IGNORE: part, desktop\n" +
                           "Music: mp3, aac, flac, ogg, wma, m4a, aiff, wav, amr\n" +
                           "Videos: flv, ogv, avi, mp4, mpg, mpeg, 3gp, mkv, ts, webm, vob, wmv\n" +
                           "Pictures: png, jpeg, gif, jpg, bmp, svg, webp, psd, tiff\n" +
                           "Archives: rar, zip, 7z, gz, bz2, tar, dmg, tgz, xz, iso, cpio\n" +
                           "Documents: txt, pdf, doc, docx, odf, xls, xlsv, xlsx, " +
                           "ppt, pptx, ppsx, odp, odt, ods, md, json, csv\n" +
                           "Books: mobi, epub, chm\n" +
                           "DEBPackages: deb\n" +
                           "Programs: exe, msi\n" +
                           "RPMPackages: rpm")
        print("CONFIG file created at: "+CONFIG)

    def checkconfig(self):
        """ create a default config if not available """
        if not os.path.isdir(os.path.dirname(CONFIG)):
            os.makedirs(os.path.dirname(CONFIG))
        if not os.path.isfile(CONFIG):
            self.create_default_config()

        with open(CONFIG, 'r') as file:
            for items in file:
                spl = items.replace('\n', '').split(':')
                key = spl[0].replace(" ","")
                val = spl[1].replace(" ","")
                self.formats[key] = val
        return

    def moveto(self, filename, from_folder, to_folder):
        from_file = os.path.join(from_folder, filename)
        to_file = os.path.join(to_folder, filename)
        # to move only files, not folders
        if not to_file == from_file:
            print('moved: ' + str(to_file))
            if os.path.isfile(from_file):
                if not os.path.exists(to_folder):
                    os.makedirs(to_folder)
                os.rename(from_file, to_file)
        return

    def classify(self, formats, output, directory):
        for file in os.listdir(directory):
            tmpbreak = False
            # set up a config per folder
            if not file == DIRCONFFILE and os.path.isfile(os.path.join(directory, file)):
                filename, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower().replace('.', '')
                if 'IGNORE' in self.formats:
                    for ignored in self.formats['IGNORE'].replace('\n', '').split(','):
                        if file_ext == ignored:
                            tmpbreak = True
                if not tmpbreak:
                    for folder, ext_list in list(formats.items()):
                        # never move files in the ignore list
                        if not folder == 'IGNORE':
                            folder = os.path.join(output, folder)
                            # make sure we are passing a list to the extension checker
                            if type(ext_list) == str:
                                ext_list = ext_list.split(',')
                            for tmp_ext in ext_list:
                                if file_ext == tmp_ext:
                                    try:
                                        self.moveto(file, directory, folder)
                                    except Exception as e:
                                        print('Cannot move file - {} - {}'.format(file, str(e)))
            """
            elif os.path.isdir(os.path.join(directory, file)) and self.args.recursive:
                self.classify(self.formats, output, os.path.join(directory, file))
            """
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

        return

    def _format_text_arg(self, arg):
        """ Set a date format to name your folders"""
        if not isinstance(arg, str):
            arg = arg.decode('utf-8')
        return arg

    def _format_arg(self, arg):
        if isinstance(arg, str):
            arg = self._format_text_arg(arg)
        return arg

    def run(self):
        if self.args.version:
            # Show version information and quit
            print(VERSION)
            return False

        if self.args.types:
            # Show file format information then quit
            for key, value in self.formats.items():
                print(key + ': '+ value)
            return False

        if self.args.edittypes:
            if PLATFORM == 'darwin':
                subprocess.call(('open', '-t', CONFIG))
            elif PLATFORM == 'win32' or OS == 'nt':
                os.startfile(CONFIG)
            elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
                subprocess.Popen(['xdg-open', CONFIG])
            return False

        if self.args.reset:
            self.create_default_config()
            return

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

        # Check for a config file in the source file directory
        if self.args.directory:
            if os.path.isfile(os.path.join(self.args.directory, DIRCONFFILE)):
                self.dirconf = os.path.join(self.args.directory, DIRCONFFILE)
        elif os.path.isfile(os.path.join(os.getcwd(), DIRCONFFILE)):
            self.dirconf = os.path.join(os.getcwd(), DIRCONFFILE)

        if self.args.dateformat:
            if not self.args.date:
                print(
                    'Dateformat -df must be given alongwith date -dt option')
                sys.exit()

        if self.args.date:
            if self.args.dateformat:
                self.classify_by_date(self.args.dateformat, output, directory)
            else:
                self.classify_by_date(self.dateformat, output, directory)
        elif self.dirconf and os.path.isfile(self.dirconf):
            print('Found config in current directory')
            if self.args.output:
                print('Your output directory is being ignored!!!')
            for items in open(self.dirconf, "r"):
                # reset formats for individual folders
                self.formats = {}
                try:
                    (key, dst, val) = items.split(':')
                    self.formats[key] = val.replace('\n', '').split(',')
                    print("\nScanning:  " + directory +
                          "\nFor:       " + key +
                          '\nFormats:   ' + val)
                    self.classify(self.formats, dst, directory)
                except ValueError:
                    print("Your local config file is malformed. Please check and try again.")
                    return False
        else:
            print("\nScanning Folder: " + directory)
            if self.args.specific_types:
                print("For: " + str(self.formats.items()))
            else:
                print("Using the default CONFIG File\n")
            self.classify(self.formats, output, directory)

        print("Done!\n")
        return True

