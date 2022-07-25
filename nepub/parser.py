import html
from html.parser import HTMLParser
import re
from typing import List
from nepub.type import Chapter


PARAGRAPH_ID_PATTERN = re.compile(r'L[1-9][0-9]*')
EPISODE_ID_PATTERN = re.compile(r'/[a-z0-9]+/([1-9][0-9]*)/')


class NarouEpisodeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.paragraphs: List[str] = []
        self._id_stack: List[str | None] = [None]
        self._classes_stack: List[List[str] | None] = [None]

    def reset(self):
        super().reset()
        self.title = ''
        self.paragraphs = []
        self._id_stack = [None]
        self._classes_stack = [None]
        self._current_paragraph = ''

    def handle_starttag(self, tag, attrs):
        # id と classes をスタックに積む
        id_flg = False
        class_flg = False
        for attr in attrs:
            if attr[0] == 'id':
                self._id_stack.append(attr[1])
                id_flg = True
            if attr[0] == 'class':
                self._classes_stack.append(attr[1].split())
                class_flg = True
        if not id_flg:
            self._id_stack.append(None)
        if not class_flg:
            self._classes_stack.append(None)

    def handle_endtag(self, tag):
        # 空の段落は読み飛ばす
        if tag == 'p' and self._current_paragraph:
            self.paragraphs.append(self._current_paragraph)
            self._current_paragraph = ''
        # id と classes をスタックからおろす
        self._id_stack.pop()
        self._classes_stack.pop()

    def handle_data(self, data):
        # paragraph
        if self._id_stack[-1] is not None and PARAGRAPH_ID_PATTERN.fullmatch(self._id_stack[-1]):
            self._current_paragraph += html.escape(data.rstrip())
        # title
        if self._classes_stack[-1] is not None and 'novel_subtitle' in self._classes_stack[-1]:
            self.title += html.escape(data.rstrip())


class NarouIndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.author = ''
        self.chapters: List[Chapter] = [{
            'name': 'default',
            'episodes': []
        }]
        self._classes_stack: List[List[str] | None] = [None, None]
        self._current_chapter: str = ''

    def handle_starttag(self, tag, attrs):
        # classes をスタックに積む
        class_flg = False
        for attr in attrs:
            if attr[0] == 'class':
                self._classes_stack.append(attr[1].split())
                class_flg = True
        if not class_flg:
            self._classes_stack.append(None)
        # 直前のタグの class に subtitle があれば href から episode_id を取り出す
        if self._classes_stack[-2] is not None and 'subtitle' in self._classes_stack[-2]:
            for attr in attrs:
                if attr[0] == 'href':
                    m = EPISODE_ID_PATTERN.fullmatch(attr[1])
                    if not m:
                        raise Exception(f'episode_id が認識できませんでした: {attr[1]}')
                    self.chapters[-1]['episodes'].append({
                        'id': m.group(1),
                        'title': '',
                        'paragraphs': [],
                    })

    def handle_endtag(self, tag):
        if tag == 'div' and self._current_chapter:
            self.chapters.append({
                'name': self._current_chapter,
                'episodes': []
            })
            self._current_chapter = ''
        # classes をスタックからおろす
        self._classes_stack.pop()

    def handle_data(self, data):
        # title
        if self._classes_stack[-1] is not None and 'novel_title' in self._classes_stack[-1]:
            self.title += html.escape(data.rstrip())
        # author
        if self._classes_stack[-2] is not None and 'novel_writername' in self._classes_stack[-2]:
            self.author += html.escape(data.rstrip())
        # chapter
        if self._classes_stack[-1] is not None and 'chapter_title' in self._classes_stack[-1]:
            self._current_chapter += html.escape(data.rstrip())
