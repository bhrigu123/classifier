import os
import sys
import arrow
import format_specifications

class Classifier(object):

    formats = format_specifications.formats

    def __init__(self, args):

        if not self.validate_args(args):
            sys.exit()

        self.args = args
        self.date_format = 'DD-MM-YYYY'
        self.output = os.getcwd() if self.args.output is None else self.args.output
        self.current_dir = os.getcwd()

        # filter out paths that are not files.
        self.files = filter(os.path.isfile, os.listdir(self.current_dir))

        if self.args.date:
            self.classify_by_date()
        else:
            self.classify()

    def classify(self):
        print ("Scanning Files")

        for file in self.files:
            filename, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()

            for folder, ext_list in list(self.formats.items()):
                folder = os.path.join(self.output, folder)
                if file_ext in ext_list:
                    self.moveto(file, self.current_dir, folder)
        print ("Done!")

    def classify_by_date(self):
        print ("Scanning Files")

        creation_dates = \
                map(lambda x: (x, arrow.get(os.path.getctime(x))), self.files)

        for file, creation_date in creation_dates:
            folder = creation_date.format(self.date_format)
            self.moveto(file, self.current_dir, folder)
        print ("Done!")

    def moveto(self, file, from_folder, to_folder):
        from_file = os.path.join(from_folder, file)
        to_file = os.path.join(to_folder, file)
        if not os.path.exists(to_folder):
            os.makedirs(to_folder)
        os.rename(from_file, to_file)

    def validate_args(self, args):
        if bool(args.specific_folder) ^ bool(args.specific_types):
            print('Specific Folder and Specific Types need to be specified together')
            return False
        elif args.specific_folder and args.specific_types:
            self.formats = {args.specific_folder: args.specific_types}
            return True
        else:
            return True
