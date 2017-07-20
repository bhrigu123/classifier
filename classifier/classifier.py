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
import os
import subprocess
from sys import platform


VERSION = 'Classifier 2.0'
DIRCONFFILE = '.classifier.conf'
PLATFORM = platform
OS = os.name
DEFAULT = """
Audio: aa, aac, aiff, amr, dvf, flac, gsm, m4a, m4b, m4p, midi, mp3, msv, ogg, ra, wav, wma
Ringtones: m4r, mmf, srt
Videos: 3g2, 3gp, amv, avi, flv, f4a, f4p, f4v, gifv, m4p, m4v, mkv, mp2, mp4, mpeg, mpg, ogv, rm, svi, ts, vob, webm, wmv
Pictures: bmp, bpg, gif, ico, jpeg, jpg, odg, png, psd, rgbe, svg, tiff, webp, vml
Archives: 7z, bz2, cpio, dmg, gz, iso, lz, rar, tar, tgz, xz, zip
Documents: ai, atom, doc, docx, kdb, kdbx, odf, odm, odp, ods, odt, pdf, ppsx, ppt, pptx, pub, qif, rtf, sxw, xls, xlsv, xlsx, xml, xt
Webpages: asp, aspx, cgi, htm, html, xhtml
Programming: a, c, cljs, coffee, class, d, e, el, erb, fth, go, java, js, lua, lisp, m, o, p, php, pl, pm, py, pyc, pyo, r, rb, so, tcl
Plain Text: asc, cer, cfg, conf, crt, css, csv, ini, inf, json, log, md, pem, pub, ppk, ssh, txt, xml, yaml
Books: chm, epub, fb2, mobi
Packages: deb, ebuild, jar, rpm
Programs: bat, cmd, com, exe, msi, out, sh, vbs
"""


if PLATFORM == 'darwin':
    CONFIG = os.path.join(os.path.expanduser('~'), '.classifier-master.conf')
elif PLATFORM == 'win32' or OS == 'nt':
    CONFIG = os.path.join(os.getenv('userprofile'), 'classifier-master.conf')
elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
    CONFIG = os.path.join(os.getenv('HOME'), '.classifier-master.conf')
else:
    CONFIG = os.path.join(os.getcwd(), '.classifier-master.conf')

class Classifier:
    """
    All format lists were taken from wikipedia, not all were added due to extensions
    not being exclusive to one format such as webm, or raw
    Audio           -       https://en.wikipedia.org/wiki/Audio_file_format
    Ringtones       -       https://en.wikipedia.org/wiki/Ringtone#Ring_tone_encoding_formats
    Images          -       https://en.wikipedia.org/wiki/Image_file_formats
    Video           -       https://en.wikipedia.org/wiki/Video_file_format
    Documents       -       https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
                            https://en.wikipedia.org/wiki/Document_file_format
    Others          -       https://en.wikipedia.org/wiki/List_of_file_formats
    """

    def __init__(self):
        self.prog=VERSION
        self.description = "Organize files in your directory into different folders"
        self.parser = argparse.ArgumentParser(description=self.description)

        self.parser.add_argument("-v", "--version", action='store_true',
                                 help="Show version and exit")
        
        self.parser.add_argument("-V", "--verbose", action='store_true',
                                 help="List every file moved")

        self.parser.add_argument("-e", "--edit", action='store_true',
                                 help="Edit the config file")

        self.parser.add_argument("-c", "--config", action='store_true',
                                 help="Show the current config file")

        self.parser.add_argument("-R", "--reset", action='store_true',
                                 help="Reset the default config file")

        self.parser.add_argument("-s", "--show-default", action='store_true',
                                  help="Show the default config file")
        
        """
        self.parser.add_argument("-r", "--recursive", action='store_true',
                                 help="Recursively search your source directory. " +
                                 "WARNING: Ensure you use the correct path as this " +
                                 "WILL move all files from your selected types.")
        """        

        self.parser.add_argument("-T", "--specific-types", type=str, nargs='+',
                                 help="Move the extensions given into the Specific Folder")

        self.parser.add_argument("-F", "--specific-folder", type=str,
                                 help="Folder to move Specific File Type")

        self.parser.add_argument("directory", type=str,
                                 help="The directory whose files to classify")
        
        self.parser.add_argument("-o", "--output", type=str, # default=self.args.directory  doesn't work yet
                                 help="Main directory to put organized folders")
        
        self.parser.add_argument("-d", "--date", action='store_true',
                                 help="Organize files by creation date")

        self.parser.add_argument("-f", "--format", type=str,
                                 help="set the date format using YYYY, MM or DD")

        self.args = self.parser.parse_args()
        self.dateformat = 'YYYY-MM-DD'
        self.formats = {}
        self.dirconf = None
        self.checkconfig()
        self.run()

    def create_default_config(self):
        with open(CONFIG, "w") as conffile:
            conffile.write(DEFAULT)
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

    def moveto(self, filename, from_folder, to_folder):
        from_file = os.path.join(from_folder, filename)
        to_file = os.path.join(to_folder, filename)
        if not os.path.isfile(from_file):
            raise OSError(from_file + " is not a file.")
        if to_file == from_file:
            raise ValueError(from_file + " is the same as destination " + to_file)
        if not os.path.exists(to_folder):
            os.makedirs(to_folder)
        os.rename(from_file, to_file)
        if self.args.verbose:
            print('moved: ' + str(to_file))

    def classify(self, formats, output, directory):
        if not any(os.isfile for file in os.listdir(directory)): # and not self.args.recursive
            if self.args.verbose:
                print("No files moved.")
            quit()
        for file in os.listdir(directory):
            """
            if os.path.isdir(os.path.join(directory, file)) and self.args.recursive:
                self.classify(self.formats, output, os.path.join(directory, file))
            """
            if os.path.isdir(os.path.join(directory, file)) or file == DIRCONFFILE:
                continue
            file_ext = os.path.splitext(file)[1].lower().replace('.', '')
            for folder, ext_list in list(formats.items()):
                # make sure we are passing a list to the extension checker
                if type(ext_list) == str:
                    ext_list = ext_list.split(',')
                if file_ext in ext_list:
                    try:
                        dest_folder = os.path.join(output, folder)
                        self.moveto(file, directory, dest_folder)
                    except OSError:
                        raise OSError('Cannot move file {} to {}'.format(file, dest_folder))

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

    def run(self):

        if self.args.version:
            print(VERSION)
            quit()

        if self.args.config:
            # Show config info then quit
            for key, value in self.formats.items():
                print(key + ': '+ value)
            quit()

        if self.args.edit:
            if PLATFORM == 'darwin':
                subprocess.call(('open', '-t', CONFIG))
            elif PLATFORM == 'win32' or OS == 'nt':
                os.startfile(CONFIG)
            elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
                subprocess.Popen(['xdg-open', CONFIG])
            quit()

        if self.args.reset:
            self.create_default_config()
            quit()
            
        if self.args.show_default:
            print(DEFAULT)
            quit()

        if bool(self.args.specific_folder) ^ bool(self.args.specific_types):
            print('Specific Folder and Specific Types need to be specified together')
            quit()

        if self.args.specific_folder and self.args.specific_types:
            self.formats = {self.args.specific_folder: self.args.specific_types}

        if self.args.output is None:
            output = self.args.directory
        else:
            output = self.args.output

        # Check for a config file in the source file directory
        if self.args.directory and os.path.isfile(os.path.join(self.args.directory, DIRCONFFILE)):
            self.dirconf = os.path.join(self.args.directory, DIRCONFFILE)

        if self.args.format and not self.args.date:
            print('Dateformat -f must be given along with date -d option')
            return False

        if self.args.date:
            try:
                import arrow
            except ImportError:
                print("You must install arrow using 'pip install arrow' to use date formatting.")
                return False
            if self.args.dateformat:
                self.classify_by_date(self.args.dateformat, output, directory)
            else:
                self.classify_by_date(self.dateformat, output, directory)
        elif self.dirconf and os.path.isfile(self.dirconf):
            print('Using config in current directory')
            if self.args.output:
                print('Config in output directory is being ignored')
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
        
        directory = self.args.directory
        if self.args.output is None:
            output = directory
            
        print("\nScanning Folder: " + directory)
        if self.args.specific_types:
            print("For: " + str(self.formats.items()))
        else:
            print("Using the default CONFIG File\n")
        self.classify(self.formats, output, directory)
        print("Done!")
        return True

if __name__ == "__main__":
    Classifier()
