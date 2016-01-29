#!/usr/bin/env python

import os

#list of known formats here can be added
"""
All format lists were taken from wikipedia, not all of them were added due to extensions
not being exclusive to one format such as webm, or raw
Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions Majority of it is from MS Office
"""

def moveto(file, from_folder, to_folder):
	#print "Moving ",file," to ", to_folder

	if not os.path.exists(to_folder):
            os.makedirs(to_folder)

	from_file	=	os.path.join(from_folder, file)
	to_file		=	os.path.join(to_folder, file)

	os.rename(from_file,to_file)

def classify(formats, output):

	print("Scanning Files")

	directory = os.getcwd()

	for file in os.listdir(directory):
		filename, file_ext = os.path.splitext(file)
		file_ext = file_ext.lower()

		for folder, ext_list in list(formats.items()):

			folder = os.path.join(output, folder)

			if file_ext in ext_list:
				moveto(file, directory, folder)

	print("Done!")
