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
  -i, --illustration    Include illustrations
  -o <file>, --output <file>
                        Output file name. If not specified, ${novel_id}.epub is used. Update the file if it exists.
```

Example:

```sh
$ nepub xxxx
noval_id: xxxx, illustration: False, output: xxxx.epub
xxxx.epub found. Loading metadata for update.
3 episodes found.
Start downloading...
Download skipped (already up to date) (1/3): https://ncode.syosetu.com/xxxx/1/
Download skipped (already up to date) (2/3): https://ncode.syosetu.com/xxxx/2/
Downloading (3/3): https://ncode.syosetu.com/xxxx/3/
Download is complete! (new: 1, skipped: 2)
Updated xxxx.epub.
```

※ xxxx の部分には小説ページの URL の末尾部分 (`https://ncode.syosetu.com/{ここの文字列}/`) に置き換えてください。

## 免責事項

自分が使う用に作ったものなので、最低限読めるものを出力する機能しかありません。

ご使用の際は、小説家になろうのサーバーに負荷をかけないよう注意してください。

このツールを使ったことによって生じた結果について、いかなる責任も負いません。 ご使用は自己責任でお願いします。
