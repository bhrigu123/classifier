# Classifier
Organize files in your current directory, by classifying them into folders of music, pdfs, images, etc.

## Installation
```sh
$ sudo pip install classifier
```

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
###Before:
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
│   ├── archive.7z
```

###After:
```
Downloads
│   ├── Music
│   │   └── 21 Guns.mp3
│   │   ├── Sultans of Swing.mp3
|	|
│   ├── Documents
│   │   └── project.docx
│   │   └── report.pdf
│   │   ├── charts.pdf
│   ├── Archives
│   │   └── CKEditor.zip
│   │   └── archive.7z
│   ├── Pictures
│   │   └── VacationPic.png
│   │   └── Cats.jpg
```


##Options
`classifier [-h] [-st SPECIFIC_TYPES [SPECIFIC_TYPES ...]] 
			[-sf SPECIFIC_FOLDER] [-o OUTPUT]`
## -h --help
show help message and exit

## -st --specific-types
Move all file extensions, given in the args list, in the current directory into the Specific Folder

## -sf --specific-folder
Folder to move files with Specific Type

## -o --output
Main directory to put organized folders

###Example
`classifier -st .py .pyc -sf Python Files`

###Before
```
Workspace
│   ├── views.py
│   ├── temp.pyc
│   ├── game.java
│   ├── index.html
│   ├── script.py
```


###After
```
Workspace
│   ├── Python Files
│   │   └── views.py
│   │   ├── temp.pyc
|	|	├── script.py
|	|
|	├── game.java
|	├── index.html

```

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
