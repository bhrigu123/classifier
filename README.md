
# Classifier
Organize files in your current directory, by classifying them into folders of music, pdfs, images, etc.

## Installation
```
#!/bin/sh
$ pip install classifier
```
#### Compatibility
* Python 2.7 / Python 3.4
* Linux / OSX / Windows


## Usage
```
$ python classifier
usage: classifier.py [-h] [-v] [-V] [-e] [-c] [-R] [-s]
                     [-T SPECIFIC_TYPES [SPECIFIC_TYPES ...]]
                     [-F SPECIFIC_FOLDER] [-o OUTPUT] [-d] [-u] [-f FORMAT]
                     directory
classifier.py: error: too few arguments

$ python classifier .
>> Scanning Folder: .
>> Done!
```

## Example
### Before:
```
Downloads
│   ├── project.docx
│   ├── 21 Guns.mp3
│   ├── Sultans of Swing.mp3
│   ├── report.pdf
│   ├── charts.pdf
│   ├── VacationPic.png
│   ├── CKEditor.zip
│   ├── Cats.jpg
│   └── archive.7z
```

### After:
```
Downloads
│   ├── Music
│   │   ├── 21 Guns.mp3
│   │   └── Sultans of Swing.mp3
|   |
│   ├── Documents
│   │   ├── project.docx
│   │   ├── report.pdf
│   │   └── charts.pdf
|   |
│   ├── Archives
│   │   ├── CKEditor.zip
│   │   └── archive.7z
|   |
│   ├── Pictures
│   │   ├── VacationPic.png
│   │   └── Cats.jpg
```


## Options
```
usage: classifier.py [-h] [-v] [-V] [-e] [-c] [-R] [-s]
                     [-T SPECIFIC_TYPES [SPECIFIC_TYPES ...]]
                     [-F SPECIFIC_FOLDER] [-o OUTPUT] [-d] [-u] [-f FORMAT]
                     directory

Organize files in your directory into different folders

positional arguments:
  directory             The directory whose files to classify

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version and exit
  -V, --verbose         List every file moved
  -e, --edit            Edit the config file
  -c, --config          Show the current config file
  -R, --reset           Reset the default config file
  -s, --show-default    Show the default config file
  -T, --specific-types SPECIFIC_TYPES [SPECIFIC_TYPES ...]
                        Move the extensions given into the Specific Folder
  -F --specific-folder SPECIFIC_FOLDER
                        Folder to move Specific File Type
  -o --output OUTPUT
                        Main directory to put organized folders
  -u, --undo            Revert all file changes since Classifier was last run
  -d, --date            Organize files by creation date
  -f, --format FORMAT
                        set the date format using YYYY, MM or DD
```



### Example
###### Classify specific file types
`classifier -st py pyc -sf "Python Files"`

### Before
```
Workspace
│   ├── views.py
│   ├── temp.pyc
│   ├── game.java
│   ├── index.html
│   └── script.py
```


### After
```
Workspace
│   ├── Python Files
│   │   ├── views.py
│   │   ├── temp.pyc
|   |   └── script.py
|   |
|   ├── game.java
|   └── index.html

```

### Example
###### Classify by Date:
`classifier -i .`

### Example
###### Classify files of directory '/home/source' and put them in location '/home/dest':
`classifier -o /home/dest /home/source`

`Note: ` If a source directory is given without -o (output) directory, this will classify the files in-place.

### View the CONFIG, how files will be sorted
`classifier -c`

### Edit the CONFIG, to set up manual settings for classification
`classifier -e`

### Reset the CONFIG file
`classifier -r`

======

## The MIT License
> Copyright (c) 2015 Bhrigu Srivastava http://bhrigu123.github.io

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
