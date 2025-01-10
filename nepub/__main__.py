import argparse
import datetime
import time
from typing import List, Tuple
from importlib.metadata import version
from nepub.epub import compose, container, content, nav, style, text
from nepub.http import get
from nepub.parser import NarouEpisodeParser, NarouIndexParser
from nepub.type import Episode

__version__ = version("nepub")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("novel_id", help="novel id", type=str)
    parser.add_argument(
        "-o",
        "--output",
        metavar="<file>",
        help="output file name",
        type=str,
        default="default.epub",
    )
    args = parser.parse_args()
    convert_narou_to_epub(args.novel_id, args.output)


def convert_narou_to_epub(novel_id: str, output: str):
    print(f"noval_id: {novel_id}, output: {output}")

    # index
    index_parser = NarouIndexParser()
    index_parser.feed(
        get(
            f"https://ncode.syosetu.com/{novel_id}/",
            {"User-agent": f"nepub/{__version__}"},
        )
    )
    title = index_parser.title
    author = index_parser.author
    created_at = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    chapters = index_parser.chapters

    # episode
    episodes: List[Episode] = []
    episode_parser = NarouEpisodeParser()
    for chapter in chapters:
        for episode in chapter["episodes"]:
            episodes.append(episode)

    print(f"{len(episodes)} episodes found.")
    print("Start downloading...")

    for i, episode in enumerate(episodes):
        print(
            f'Downloading ({i + 1}/{len(episodes)}): https://ncode.syosetu.com/{novel_id}/{episode["id"]}/'
        )
        episode_parser.feed(
            get(
                f'https://ncode.syosetu.com/{novel_id}/{episode["id"]}/',
                {"User-agent": f"nepub/{__version__}"},
            )
        )
        episode["title"] = episode_parser.title
        episode["paragraphs"] = episode_parser.paragraphs
        episode_parser.reset()
        # 負荷かけないようにちょっと待つ
        time.sleep(1)

    print("Download is complete!")

    # files
    files: List[Tuple[str, str]] = []
    files.append(("mimetype", "application/epub+zip"))
    files.append(("META-INF/container.xml", container()))
    files.append(("src/style.css", style()))
    files.append(("src/content.opf", content(title, author, created_at, episodes)))
    files.append(("src/navigation.xhtml", nav(chapters)))
    for episode in episodes:
        files.append(
            (
                f'src/text/{episode["id"]}.xhtml',
                text(episode["title"], episode["paragraphs"]),
            )
        )
    compose(output, files)

    print(f"Created {output}.")


if __name__ == "__main__":
    main()
