from unittest import TestCase
from nepub.parser import NarouEpisodeParser, NarouIndexParser


class TestNarouEpisodeParser(TestCase):
    def test_narou_episode_parser(self):
        parser = NarouEpisodeParser()
        parser.feed('''
        <p class="novel_subtitle class1">タイトル</p>
        <p id="L1">段落1</p>
        <p id="L2">段落2</p>
        ''')
        self.assertEqual('タイトル', parser.title)
        self.assertEqual(['段落1', '段落2'], parser.paragraphs)


class TestNarouIndexParser(TestCase):
    def test_narou_index_parser(self):
        parser = NarouIndexParser()
        parser.feed('''
        <p class="novel_title class1">タイトル</p>
        <div class="novel_writername class1">
            作者：<a href="https://mypage.syosetu.com/xxxx/">作者</a>
        </div>
        <div class="chapter_title class1">チャプター1</div>
        <dd class="subtitle class1">
            <a href="/xxxx/1/">エピソード1</a>
        </dd>
        <dd class="subtitle class1">
            <a href="/xxxx/2/">エピソード2</a>
        </dd>
        <div class="chapter_title class1">チャプター2</div>
        <dd class="subtitle class1">
            <a href="/xxxx/3/">エピソード3</a>
        </dd>
        ''')
        self.assertEqual('タイトル', parser.title)
        self.assertEqual('作者', parser.author)
        self.assertEqual([{
            'name': 'default',
            'episodes': []
        }, {
            'name': 'チャプター1',
            'episodes': [
                {
                    'id': '1',
                    'title': '',
                    'paragraphs': []
                }, {
                    'id': '2',
                    'title': '',
                    'paragraphs': []
                }
            ]
        }, {
            'name': 'チャプター2',
            'episodes': [
                {
                    'id': '3',
                    'title': '',
                    'paragraphs': []
                }
            ]
        }], parser.chapters)
