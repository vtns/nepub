from nepub.parser import NarouEpisodeParser


if __name__ == '__main__':
    parser = NarouEpisodeParser()
    parser.feed('''
    <p class="novel_subtitle">title</p>
    <p id="L1">aaaa</p>
    <p id="L2">bbbb</p>
    ''')

    print(parser.title)
    print(parser.paragraphs)
