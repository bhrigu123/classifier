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
import sys


VERSION = 'Classifier 2.0'
DIRCONFFILE = '.classifier.conf'
PLATFORM = sys.platform
OS = os.name
HELP = """usage: classifier DIRECTORY
    -h, --help"""
DEFAULT = """Audio: aa, aac, aiff, amr, dvf, flac, gsm, m4a, m4b, m4p, midi, mp3, msv, ogg, ra, wav, wma
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

        self.parser.add_argument("-n", "--no-save", action='store_true',
                                 help="Run without saving the current directory. Undo will not be available.")

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

        self.parser.add_argument("directory", type=str, nargs='?',
                                 help="The directory to classify")
        
        self.parser.add_argument("-o", "--output", type=str, # default=self.args.directory  doesn't work yet
                                 help="Directory to put organized folders")
        
        self.parser.add_argument("-d", "--date", action='store_true',
                                 help="Organize files by creation date")

        self.parser.add_argument("-u", "--undo", action='store_true',
                                 help="Revert all file changes since Classifier was last run")

        self.parser.add_argument("-f", "--format", type=str,
                                 help="Set a specific date format")

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
            os.mkdir(os.path.dirname(CONFIG))
        if not os.path.isfile(CONFIG):
            self.create_default_config()
        with open(CONFIG, 'r') as file:
            for line in file:
                spl = line.replace('\n', '').split(':')
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
            
    def save_current(self, directory):
        self.import_git()
        repo = self.git.Repo.init(directory)  # works even if repo already exists
        repo.git.add('--all', '--force')
        repo.git.commit('--author="Classifier <https://github.com/jyn514/classifier>"',
                        '--message="Saved by classifier.py to allow an undo function."',
                        '--quiet')
        
    def undo(self, directory, commit=1):
        # commit is an integer referring to previous revisions
        self.import_git()
        repo = self.git.Repo.init(directory)
        log = repo.git.log('--author="Classifier"', '--pretty="oneline"').split('\n')
        sha_sums = [i[:i.index(' ')] for i in log]      # remove commit message
        repo.git.checkout('--force', sha_sums[-commit])

    def import_git(self):
        try:
            import git
            self.git = git
        except ImportError:
            raise ImportError("You must install both git and gitpython to use the undo " +
                  "function, using `apt install git` and `pip install gitpython`.")

    def classify(self, formats, output, directory):
        if not any(os.path.isfile for file in os.listdir(directory)): # and not self.args.recursive
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

    def classify_by_date_arrow(self, date_format, output, directory, files):
        creation_dates = map(lambda x: (x, self.arrow.get(os.path.getctime(os.path.join(directory, x)))), files)
        for file, creation_date in creation_dates:
            folder = os.path.join(output, creation_date.format(date_format))
            self.moveto(file, directory, folder)

    def classify_by_date_no_arrow(self, date_format, output, directory, files):
        creation_times_since_epoch = (map(lambda x: (x, os.path.getctime(os.path.join(directory, x)))), files)
        for file, creation_time in creation_times_since_epoch:
            folder = os.path.join(output, time.strftime(date_format, time.ctime(creation_time)))
            self.moveto(file, directory, folder)
            
    def run(self):

        if self.args.version:
            quit(VERSION)

        if self.args.config:
            with open(CONFIG, 'r') as f:
                f.readlines()
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
            quit(DEFAULT)

        if bool(self.args.specific_folder) ^ bool(self.args.specific_types):
            quit('Specific Folder and Specific Types need to be specified together')

        if not self.args.directory:
            quit(HELP)
            
        directory = self.args.directory
        if self.args.output is None:
            output = directory

        if not os.path.isdir(directory):
            print("Folder {} not found.".format(directory))
            quit()

        if not self.args.no_save:
            try:
                self.save_current(directory)
            except ImportError:
                quit("Unable to undo any changes! Aborting; use --no-save if you are sure.")

        if self.args.undo:
            print("Reverting all changes since Classifier was last run. If you have " +
                  "never run Classifier, this will DELETE ALL FILES in the directory.")
            confirm = input("Type 'Yes' to continue, '?' for more info, or anything else to abort.")
            if confirm == '?':
                print("This program uses the Git program and Gitpython library to backup your files.")
                print("Each time Classifier runs, it saves the current directory in the `.git/` subfolder. ")
            elif confirm == 'Yes':
                self.undo(directory)

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
            quit('Dateformat -f must be given along with date -d option')
                
        if self.dirconf and os.path.isfile(self.dirconf):   # custom config
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
                    quit("Your local config file is malformed. Please check and try again.")
            
        elif self.args.date:    # date sort
            if self.args.format:
                self.dateformat = self.args.format
            files = [x for x in os.listdir(directory) if not x.startswith('.') and os.path.isfile(x)]
            try:
                import arrow
                self.arrow = arrow
                self.classify_by_date_arrow(self.dateformat, output, directory, files)
            except ImportError:
                print("You must install arrow using 'pip install arrow'" +
                      "to use human-readable date formatting.")
                print("Using the datetime module; formatting help available at " +
                      "https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior")
                self.classify_by_date_no_arrow(self.dateformat, output, directory, files)

        else:                   # sort by config     
            if self.args.specific_types:
                print("Using specified config: " + str(self.formats.items()))
            else:
                print("Using the default CONFIG File\n")
            self.classify(self.formats, output, directory)
        quit("Done!")

if __name__ == "__main__":
    Classifier()
