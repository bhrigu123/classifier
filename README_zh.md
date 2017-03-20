# Classifier
整理当前文件夹内的文件，把它们分类到 music, pdfs, images 等目录中。

## 安装
```sh
$ pip install classifier
```
#### 平台兼容性
* Python 2.7 / Python 3.4
* Linux / OSX / Windows


## 使用说明
* 到需要整理分类的目录中自行下面的指令 
```sh
$ classifier
```
```sh
>> Scanning Files
>> Done!
```

## 示例
### 整理前:
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

###整理后:
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


##选项
`classifier [-dt] [-st SPECIFIC_TYPES [SPECIFIC_TYPES ...]] [-sf SPECIFIC_FOLDER] [-o OUTPUT]`

	-h --help				显示帮助
	-dt --date				按日期归类文件
	-st --specific-types	将某个扩展名的文件归类
	-sf --specific-folder	归类到的目录
	-d --directory		    需要整理的目录
	-o --output				输出目录
    -c --config             配置文件,默认是 `~/.config/classifier`

### 示例
###### 整理文件的扩展名以空格分割
`classifier -st .py .pyc -sf "Python Files"`

### 整理前:
```
Workspace
│   ├── views.py
│   ├── temp.pyc
│   ├── game.java
│   ├── index.html
│   └── script.py
```


###整理后:
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

### 示例
###### 按日期整理:
`classifier -dt`

### 示例
###### 将 `/home/source` 目录下的文件分类整理到 `/home/dest` 目录:
`classifier -d /home/source -o /home/dest`

`Note: ` 如果只是通过 `-d` 设置了需要整理的目录，没有通过 `-o` 设置输出目录, 输出目录会使用 `-d` 设置的整理目录. 例如:<br>
`classifier -d /home/source'` <br>
在 `/home/source` 下进行归类整理.



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
