
"""
All format lists were taken from wikipedia, not all of them were added due to extensions
not being exclusive to one format such as webm, or raw
Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
"""

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
