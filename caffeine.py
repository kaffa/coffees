"""
MIT License

Copyright (c) 2024 kaffa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
## 说明

本软件适用于 Windows 下使用 TiddlyWiki Single File + Github Pages 使用。它与 aio.cmd 一起使用实现写作保存后自动推送 GitHub。

## 使用方法

在保存 TiddlyWiki 条目之前，先打开命令行，进入 TiddlyWiki 目录，再运行脚本 `caffeine.py`。例如： 

```shell
cd /d d:/your-tiddlywiki-folder/
python caffeine.py
```

## 默认路径

下载目录是浏览器下载目录，也可以通过命令行参数在运行时指定：

```python
python caffeine.py /path-to-your-downloaded-tiddlywiki.html-file
```

## macOS

它很容易移植到 macOS 因为它使用 watchdog。
"""

"""
## Description

This software is applicable for using TiddlyWiki Single File + Github Pages on Windows. 

It is used together with aio.cmd to achieve the automatic push to GitHub after writing and saving.

## Usage

Before saving the TiddlyWiki entry, open the command line first, enter the TiddlyWiki directory, and then run the script `caffeine.py`. For example:

```shell
cd /d d:/your-tiddlywiki-folder/
python caffeine.py
```

## Default path

The download directory is the browser download directory, and it can also be specified at runtime through command line parameters:

```python
python caffeine.py /path-to-your-downloaded-tiddlywiki.html-file
```

## macOS

It can be easily ported to macOS as it uses watchdog.

"""
import os
import sys
import time
import re
import subprocess
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    path = sys.argv[1] if len(sys.argv) > 1 else os.getenv('USERPROFILE') + '\\Downloads'
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(3)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)

            if re.match(r"tiddlywiki \([\d+]*?\).html", event.src_path.split('\\').pop()):
                shutil.copyfile(event.src_path, 'index.html')
                subprocess.Popen(f'cmd /c "aio.cmd"', shell=True)


if __name__ == '__main__':
    w = Watcher()
    w.run()
