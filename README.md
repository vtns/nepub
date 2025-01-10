# nepub

「小説家になろう」の小説を縦書きの EPUB に変換するためのツール

## Requirements

* Python 3.7 or later

## Installation

```sh
pip install git+https://github.com/ttk1/nepub.git
```

## Usage

```sh
$ nepub -h
usage: nepub [-h] [-i] [-o <file>] novel_id

positional arguments:
  novel_id              novel id

options:
  -h, --help            show this help message and exit
  -i, --illustration    include illustrations
  -o <file>, --output <file>
                        output file name
```

Example:

```sh
$ nepub xxxx
noval_id: xxxx, output: default.epub
3 episodes found.
Start downloading...
Downloading (1/3): https://ncode.syosetu.com/xxxx/1/
Downloading (2/3): https://ncode.syosetu.com/xxxx/2/
Downloading (3/3): https://ncode.syosetu.com/xxxx/3/
Download is complete!
Created default.epub.
```

※ xxxx の部分には小説ページの URL の末尾部分 (`https://ncode.syosetu.com/{ここの文字列}/`) に置き換えてください。

## 免責事項

自分が使う用に作ったものなので、最低限読めるものを出力する機能しかありません。

ご使用の際は、小説家になろうのサーバーに負荷をかけないよう注意してください。

このツールを使ったことによって生じた結果について、いかなる責任も負いません。 ご使用は自己責任でお願いします。
