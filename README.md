# Classifier
Organize files in your current directory, by classifying them into folders of music, pdfs, images, etc.

## Installation
```sh
$ sudo pip install classifier
```

## Usage
Go to your directory, where you want to classify your files and run following command in your terminal.
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
│   ├── CKEditor.zip
```

###After:
```
Downloads
│   ├── Music
│   │   └── 21 Guns.mp3
│   │   ├── Sultans of Swing.mp3
.............................
│   ├── pdfs
│   │   └── report.pdf
│   │   ├── charts.pdf
.............................
│   ├── docs
│   │   └── project.docx
│   ├── zip
│   │   └── CKEditor.zip
│   ├── Pictures
```

## Compatibility 
* Python 2.7 / Python 3.4
* Ubuntu / OSX / Windows 

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
