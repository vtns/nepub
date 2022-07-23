from nepub.parser import NarouParser


if __name__ == '__main__':
    parser = NarouParser()
    parser.feed('''
    <p class="novel_subtitle">title</p>
    <p id="L1">aaaa</p>
    <p id="L2">bbbb</p>
    ''')

    print(parser.title)
    print(parser.paragraphs)
