from nepub.parser import NarouParser
import urllib.request


def get(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf-8')


if __name__ == '__main__':
    content = get('https://ncode.syosetu.com/n0611em/2/')
    parser = NarouParser()
    parser.feed(content)
    print(parser.title)
    print(parser.paragraphs)
