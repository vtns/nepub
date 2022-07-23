from nepub.parser import NarouEpisodeParser, NarouIndexParser
import urllib.request


def get(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as res:
        return res.read().decode('utf-8')


if __name__ == '__main__':
    content = get('https://ncode.syosetu.com/n7975cr/')
    index_parser = NarouIndexParser()
    index_parser.feed(content)
    print(index_parser.title)
    print(index_parser.author)
    print(index_parser.chapters)

    content = get('https://ncode.syosetu.com/n0611em/2/')
    episode_parser = NarouEpisodeParser()
    episode_parser.feed(content)
    print(episode_parser.title)
    print(episode_parser.paragraphs)
