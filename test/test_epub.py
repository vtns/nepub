from unittest import TestCase
from jinja2 import Environment, PackageLoader
from importlib import resources

from nepub.epub import content, nav, text


class TestEpub(TestCase):
    def test_content(self):
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="ja">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title id="title">たいとる</dc:title>
        <dc:creator id="creator01">作者</dc:creator>
        <dc:language>ja</dc:language>
        <meta property="dcterms:modified">2022-01-01T00:00:00Z</meta>
    </metadata>
    <manifest>
        <item media-type="application/xhtml+xml" id="nav" href="navigation.xhtml" properties="nav" />
        <item media-type="text/css" id="style" href="style.css" />
        <item media-type="application/xhtml+xml" id="001" href="text/001.xhtml" />
        <item media-type="application/xhtml+xml" id="002" href="text/002.xhtml" />
    </manifest>
    <spine page-progression-direction="rtl">
        <itemref linear="yes" idref="001" />
        <itemref linear="yes" idref="002" />
    </spine>
</package>''', content('たいとる', '作者', '2022-01-01T00:00:00Z', [
            {
                'id': '001',
                'title': 'たいとる1',
                'paragraphs': []
            }, {
                'id': '002',
                'title': 'たいとる2',
                'paragraphs': []
            }
        ]))

    def test_nav_(self):
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
    <head>
        <meta charset="UTF-8" />
        <title>Navigation</title>
    </head>
    <body>
        <nav epub:type="toc">
            <h1>Navigation</h1>
            <ol>
                <li>
                    <a href="text/001.xhtml">ちゃぷたー1</a>
                    <ol>
                        <li>
                            <a href="text/001.xhtml">たいとる1</a>
                        </li>
                        <li>
                            <a href="text/002.xhtml">たいとる2</a>
                        </li>
                    </ol>
                </li>
                <li>
                    <a href="text/003.xhtml">ちゃぷたー2</a>
                    <ol>
                        <li>
                            <a href="text/003.xhtml">たいとる3</a>
                        </li>
                    </ol>
                </li>
            </ol>
        </nav>
    </body>
</html>''', nav([
            {
                'name': 'default',
                'episodes': []
            }, {
                'name': 'ちゃぷたー1',
                'episodes': [
                    {
                        'id': '001',
                        'title': 'たいとる1',
                        'paragraphs': []
                    }, {
                        'id': '002',
                        'title': 'たいとる2',
                        'paragraphs': []
                    }
                ]
            }, {
                'name': 'ちゃぷたー2',
                'episodes': [
                    {
                        'id': '003',
                        'title': 'たいとる3',
                        'paragraphs': []
                    }
                ]
            }
        ]))

    def test_nav_default(self):
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
    <head>
        <meta charset="UTF-8" />
        <title>Navigation</title>
    </head>
    <body>
        <nav epub:type="toc">
            <h1>Navigation</h1>
            <ol>
                <li>
                    <a href="text/001.xhtml">たいとる1</a>
                </li>
                <li>
                    <a href="text/002.xhtml">たいとる2</a>
                </li>
            </ol>
        </nav>
    </body>
</html>''', nav([
            {
                'name': 'default',
                'episodes': [
                    {
                        'id': '001',
                        'title': 'たいとる1',
                        'paragraphs': []
                    }, {
                        'id': '002',
                        'title': 'たいとる2',
                        'paragraphs': []
                    }
                ]
            }
        ]))

    def test_text(self):
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja">
    <head>
        <meta charset="UTF-8" />
        <title>たいとる</title>
        <link href="../style.css" type="text/css" rel="stylesheet" />
    </head>
    <body>
        <h1>たいとる</h1>
        <p>だんらく1</p>
        <p>だんらく2</p>
    </body>
</html>''', text('たいとる', [
            'だんらく1',
            'だんらく2',
        ]))
