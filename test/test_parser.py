from unittest import TestCase
from nepub.parser import NarouEpisodeParser


class TestNarouParser(TestCase):
    def test_title_and_paragraphs(self):
        parser = NarouEpisodeParser()
        parser.feed('''
        <p class="novel_subtitle class2">title</p>
        <p id="L1">aaaa</p>
        <p id="L2">bbbb</p>
        ''')
        self.assertEqual('title', parser.title)
        self.assertEqual(['aaaa', 'bbbb'], parser.paragraphs)
