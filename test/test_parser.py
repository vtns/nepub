from unittest import TestCase
from nepub.parser import NarouEpisodeParser, NarouIndexParser


class TestNarouEpisodeParser(TestCase):
    def test_narou_episode_parser(self):
        parser = NarouEpisodeParser()
        parser.feed(
            """
            <h1 class="p-novel__title p-novel__title--rensai">タイトル</h1>
            <p id="L1">　段落1</p>
            <p id="L2"><br /></p>
            <p id="L3"></p>
            <p id="L4">「段落4」</p>
            <p id="L5">"段落5"</p>
            """
        )
        self.assertEqual("タイトル", parser.title)
        self.assertEqual(
            ["　段落1", "「段落4」", "&quot;段落5&quot;"], parser.paragraphs
        )

    def test_narou_episode_parser_ruby(self):
        parser = NarouEpisodeParser()
        parser.feed(
            """
            <h1 class="p-novel__title p-novel__title--rensai">タイトル</h1>
            <p id="L1">あああ<ruby>段落1<rt>だんらくいち</rt></ruby>あああ</p>
            <p id="L2">いいい<ruby>段落2<rp>(</rp><rt>だんらくに</rt><rp>)</rp></ruby>いいい</p>
            <p id="L3">ううう<ruby><rb>段落3<rt>だんらくさん</rt></ruby>ううう</p>
            <p id="L3">えええ<ruby><rb>段落4<rt>だんらくよん</rt></ruby>えええ</p>
            """
        )
        self.assertEqual("タイトル", parser.title)
        self.assertEqual(
            [
                "あああ<ruby>段落1<rt>だんらくいち</rt></ruby>あああ",
                "いいい<ruby>段落2<rt>だんらくに</rt></ruby>いいい",
                "ううう<ruby>段落3<rt>だんらくさん</rt></ruby>ううう",
                "えええ<ruby>段落4<rt>だんらくよん</rt></ruby>えええ",
            ],
            parser.paragraphs,
        )


class TestNarouIndexParser(TestCase):
    def test_narou_index_parser(self):
        parser = NarouIndexParser()
        parser.feed(
            """
            <h1 class="p-novel__title">タイトル</h1>
            <div class="p-novel__author">
                作者：<a href="https://mypage.syosetu.com/xxxx/">作者</a>
            </div>
            <span class="c-pager__item c-pager__item--first">最初へ</span>
            <span class="c-pager__item c-pager__item--before">前へ</span>
            <a href="/xxxx/?p=2" class="c-pager__item c-pager__item--next">次へ</a>
            <a href="/xxxx/?p=9" class="c-pager__item c-pager__item--last">最後へ</a>
            <div class="p-eplist__chapter-title">チャプター1</div>
            <div class="p-eplist__sublist">
                <a href="/xxxx/1/" class="p-eplist__subtitle">エピソード1</a>
            </div>
            <div class="p-eplist__sublist">
                <a href="/xxxx/2/" class="p-eplist__subtitle">エピソード2</a>
            </div>
            <div class="p-eplist__chapter-title">チャプター2</div>
            <div class="p-eplist__sublist">
                <a href="/xxxx/3/" class="p-eplist__subtitle">エピソード3</a>
            </div>
            """
        )
        self.assertEqual("タイトル", parser.title)
        self.assertEqual("作者", parser.author)
        self.assertEqual("/xxxx/?p=2", parser.next_page)
        self.assertEqual(
            [
                {"name": "default", "episodes": []},
                {
                    "name": "チャプター1",
                    "episodes": [
                        {"id": "1", "title": "", "paragraphs": []},
                        {"id": "2", "title": "", "paragraphs": []},
                    ],
                },
                {
                    "name": "チャプター2",
                    "episodes": [{"id": "3", "title": "", "paragraphs": []}],
                },
            ],
            parser.chapters,
        )

    def test_narou_index_parser_last_page(self):
        parser = NarouIndexParser()
        parser.feed(
            """
            <h1 class="p-novel__title">タイトル</h1>
            <div class="p-novel__author">
                作者：<a href="https://mypage.syosetu.com/xxxx/">作者</a>
            </div>
            <a href="/xxxx/" class="c-pager__item c-pager__item--first">最初へ</a>
            <a href="/xxxx/?p=9" class="c-pager__item c-pager__item--before">前へ</a>
            <span class="c-pager__item c-pager__item--next">次へ</span>
            <span class="c-pager__item c-pager__item--last">最後へ</span>
            <div class="p-eplist__sublist">
                <a href="/xxxx/999/" class="p-eplist__subtitle">エピソード1</a>
            </div>
            """
        )
        self.assertEqual("タイトル", parser.title)
        self.assertEqual("作者", parser.author)
        self.assertEqual(None, parser.next_page)
        self.assertEqual(
            [
                {
                    "name": "default",
                    "episodes": [
                        {"id": "999", "title": "", "paragraphs": []},
                    ],
                },
            ],
            parser.chapters,
        )
