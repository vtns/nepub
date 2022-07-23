from html.parser import HTMLParser
import re
from typing import List, TypedDict


PARAGRAPH_ID_PATTERN = re.compile(r'L[1-9][0-9]*')


class NarouEpisodeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.paragraphs: List[str] = []
        self._reset()

    def _reset(self):
        self._current_tag = ''
        self._current_classes = []
        self._current_id = None
        self._current_paragraph = ''

    def handle_starttag(self, tag, attrs):
        self._reset()
        self._current_tag = tag
        for attr in attrs:
            if attr[0] == 'id':
                self._current_id = attr[1]
            if attr[0] == 'class':
                self._current_classes = attr[1].split()

    def handle_endtag(self, tag):
        if self._current_paragraph:
            self.paragraphs.append(self._current_paragraph)

    def handle_data(self, data):
        # paragraph
        if self._current_id is not None and PARAGRAPH_ID_PATTERN.fullmatch(self._current_id):
            self._current_paragraph += data.strip()
        # title
        if 'novel_subtitle' in self._current_classes:
            self.title += data.strip()


class Chapter(TypedDict):
    name: str
    episodes: List[str]


class NarouIndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.author = ''
        self._current_classes = []
        self._previous_classes = []
        self.chapters: List[Chapter] = [{
            'name': 'default',
            'episodes': []
        }]
        self._reset()

    def _reset(self):
        self._current_tag = ''
        self._current_classes = []
        self._current_chapter = ''

    def handle_starttag(self, tag, attrs):
        self._previous_classes = self._current_classes
        self._reset()
        self._current_tag = tag
        for attr in attrs:
            if attr[0] == 'id':
                self._current_id = attr[1]
            if attr[0] == 'class':
                self._current_classes = attr[1].split()
            # episode
            if 'subtitle' in self._previous_classes and attr[0] == 'href':
                self.chapters[-1]['episodes'].append(attr[1])

    def handle_endtag(self, tag):
        if self._current_chapter:
            self.chapters.append({
                'name': self._current_chapter,
                'episodes': []
            })

    def handle_data(self, data):
        # title
        if 'novel_title' in self._current_classes:
            self.title += data.strip()
        # author
        if 'novel_writername' in self._previous_classes:
            self.author += data.strip()
        # chapter
        if 'chapter_title' in self._current_classes:
            self._current_chapter += data.strip()
