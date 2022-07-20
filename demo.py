import re
from html.parser import HTMLParser
import urllib.request
print('hello')


def get(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf-8')


#b = get('https://ncode.syosetu.com/n0611em/2/')
# print(b)


paragraph_id_pattern = re.compile(r'L[1-9][0-9]*')


class NarouParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.current_id = ''
        self.title = ''
        self.paragraphs = []

    def getTitle(self):
        return self.title

    def getParagraphs(self):
        return self.paragraphs

    def handle_starttag(self, tag, attrs):
        # self.tag_stack.append(tag)
        self.current_tag = tag
        attr_id = list(filter(lambda x: x[0] == 'id', attrs))
        print(attr_id)
        if attr_id:
            self.current_id = attr_id[0][1]
        else:
            self.current_id = None

    def handle_endtag(self, tag):
        # if self.tag_stack[-1] == tag:
        #     self.tag_stack.pop()
        # else:
        #     raise Exception('エラー')
        pass

    def handle_data(self, data):
        if data == '\n':
            # https://stackoverflow.com/questions/32262058/python-htmlparser-printing-out-blank-lines
            # handle_endtag とかでなんとかしたい
            return

        if self.current_id is not None and paragraph_id_pattern.fullmatch(self.current_id):
            print(f'{self.current_tag, self.current_id:} |{data}|')


parser = NarouParser()
# parser.feed(b)

parser.feed('''
<p id="L1">zzz</p>
<p id="L2">aaa</p>
''')
