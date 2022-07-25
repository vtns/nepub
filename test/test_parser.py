from unittest import TestCase
from nepub.parser import NarouEpisodeParser, NarouIndexParser


class TestNarouEpisodeParser(TestCase):
    def test_narou_episode_parser(self):
        parser = NarouEpisodeParser()
        parser.feed('''
        <p class="novel_subtitle class1">タイトル</p>
        <p id="L1">　段落1</p>
        <p id="L2"><br></p>
        <p id="L3"></p>
        <p id="L4">「段落4」</p>
        <p id="L5">"段落5"</p>
        ''')
        self.assertEqual('タイトル', parser.title)
        self.assertEqual(['　段落1', '「段落4」', '&quot;段落5&quot;'],
                         parser.paragraphs)

    def test_narou_episode_parser_ruby(self):
        parser = NarouEpisodeParser()
        parser.feed('''
        <p class="novel_subtitle class1">タイトル</p>
        <p id="L1">あああ<ruby>段落1<rt>だんらくいち</rt></ruby>あああ</p>
        <p id="L2">いいい<ruby>段落2<rp>（</rp><rt>だんらくに</rt><rp>）</rp></ruby>いいい</p>
        <p id="L3">ううう<ruby><rb>段落3<rt>だんらくさん</rt></ruby>ううう</p>
        <p id="L3">えええ<ruby><rb>段落4<rt>だんらくよん</rt></ruby>えええ</p>
        ''')
        self.assertEqual('タイトル', parser.title)
        self.assertEqual(['あああ<ruby>段落1<rt>だんらくいち</rt></ruby>あああ',
                          'いいい<ruby>段落2<rt>だんらくに</rt></ruby>いいい',
                          'ううう<ruby>段落3<rt>だんらくさん</rt></ruby>ううう',
                          'えええ<ruby>段落4<rt>だんらくよん</rt></ruby>えええ'],
                         parser.paragraphs)


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
