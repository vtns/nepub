# nepub

なろう小説を EPUB に変換するためのツール

## Requirements

* Python 3.7 or later

## Usage

```sh
$ nepub -h
usage: nepub [-h] [-o <file>] novel_id

positional arguments:
  novel_id              novel id

options:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        output file name
```

## Example

```sh
nepub xxxx -o example.epub
```

※ xxxx の部分には小説ページの URL の末尾部分 (`https://ncode.syosetu.com/{ここの文字列}/`) に置き換えてください。

## 注意

自分が使う用に作ったものなので、最低限読めるものを出力する機能しかありません。

利用の際は、小説家になろうのサーバーに負荷をかけないよう注意して利用してください。