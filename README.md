
# Classifier
Organize files in your current directory, by classifying them into folders of music, pdfs, images, etc.

## Installation
```sh
$ pip install classifier
```
#### Compatibility
* Python 2.7 / Python 3.4
* Linux / OSX / Windows


## Usage
* Go to your directory, where you want to classify your files.
* Run the following command in your terminal.
```sh
$ classifier
```
```sh
>> Scanning Files
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
`classifier [-dt] [-st SPECIFIC_TYPES [SPECIFIC_TYPES ...]] [-sf SPECIFIC_FOLDER] [-o OUTPUT]`

optional arguments:

```
  -h, --help            show this help message and exit
  -st SPECIFIC_TYPES [SPECIFIC_TYPES ...], --specific-types SPECIFIC_TYPES [SPECIFIC_TYPES ...]
                        Move all file extensions, given in the args list, in
                        the current directory into the Specific Folder
  -sf SPECIFIC_FOLDER, --specific-folder SPECIFIC_FOLDER
                        Folder to move Specific File Type
  -o OUTPUT, --output OUTPUT
                        Main directory to put organized folders
  -d DIRECTORY, --directory DIRECTORY
                        The directory whose files to classify
  -dt, --date           Organize files by creation date
```

> More options (given below) coming soon.

### Example
###### Classify specific file types
`classifier -st .py .pyc -sf "Python Files"`

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
|   |	└── script.py
|   |
|   ├── game.java
|   └── index.html

```

### Example
###### Classify by Date:
`classifier -dt`

### Example
###### Classify files of directory '/home/source' and put them in location '/home/dest':
`classifier -d /home/source -o /home/dest`

`Note: ` If -d (source directory) is given without -o (output) directory, this will classify the files of source directory and  the classified folders be in that source directory only. Eg:<br>
`classifier -d /home/source'`<br>
This classifies the directory /home/source.



### Coming soon - Config file and other options
```
-v, --version         show version, filename and exit
-et, --edittypes      Edit the list of types and formats
-t, --types           Show the current list of types and formats
-r, --recursive       Recursively search your source directory.
                        WARNING: Ensure you use the correct path as this
                        WILL move all files from your selected types.
```

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
