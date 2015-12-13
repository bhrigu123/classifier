# Classifier
Organize files in your current directory, by classifying them into folders of music, pdfs, images, etc.

## Installation
```sh
$ sudo pip install classifier
```

## Usage
First, go to your directory, where you want to classify your files.
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

