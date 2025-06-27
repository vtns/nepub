import argparse
import datetime
import json
import os
import tempfile
import time
import zipfile
from typing import List

from nepub.epub import container, content, nav, style, text
from nepub.http import get
from nepub.parser import NarouEpisodeParser, NarouIndexParser
from nepub.type import Episode, Image, Metadata, MetadataImage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("novel_id", help="novel id", type=str)
    parser.add_argument(
        "-i", "--illustration", help="Include illustrations", action="store_true"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="<file>",
        help="Output file name. If not specified, ${novel_id}.epub is used. Update the file if it exists.",
        type=str,
    )
    args = parser.parse_args()
    if args.output:
        output = args.output
    else:
        output = f"{args.novel_id}.epub"
    convert_narou_to_epub(args.novel_id, args.illustration, output)


def convert_narou_to_epub(novel_id: str, illustration: bool, output: str):
    print(f"novel_id: {novel_id}, illustration: {illustration}, output: {output}")

    # metadata
    metadata: Metadata | None = None
    new_metadata: Metadata = {
        "novel_id": novel_id,
        "illustration": illustration,
        "episodes": {},
    }
    if os.path.exists(output):
        print(f"{output} found. Loading metadata for update.")
        with zipfile.ZipFile(output, "r") as zf_old:
            with zf_old.open("src/metadata.json") as f:
                metadata = json.load(f)

    # check novel_id
    if metadata and metadata["novel_id"] != novel_id:
        # metadata の novel_id と値が異なる場合処理を中止する
        print(
            f'Process stopped as the novel_id differs from metadata: {metadata["novel_id"]}'
        )
        return

    # check illustration flag
    if metadata and metadata["illustration"] != illustration:
        # metadata の illustration フラグと値が異なる場合処理を中止する
        print(
            f'Process stopped as the illustration value differs from metadata: {metadata["illustration"]}'
        )
        return

    # index
    index_parser = NarouIndexParser()
    index_parser.feed(get(f"https://ncode.syosetu.com/{novel_id}/"))
    title = index_parser.title
    author = index_parser.author
    next_page = index_parser.next_page
    timestamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    chapters = index_parser.chapters
    while next_page is not None:
        index_parser.reset()
        index_parser.chapters = chapters
        index_parser.feed(get(f"https://ncode.syosetu.com/{novel_id}/?p={next_page}"))
        chapters = index_parser.chapters
        next_page = index_parser.next_page
        # 負荷かけないようにちょっと待つ
        time.sleep(1)

    # episode
    downloaded_count = 0
    skipped_count = 0
    episodes: List[Episode] = []
    images: List[Image] = []
    metadata_images: List[MetadataImage] = []
    episode_parser = NarouEpisodeParser(illustration)
    for chapter in chapters:
        for episode in chapter["episodes"]:
            episodes.append(episode)

    print(f"{len(episodes)} episodes found.")
    print("Start downloading...")

    for i, episode in enumerate(episodes):
        if metadata:
            if episode["id"] in metadata["episodes"]:
                metadata_episode = metadata["episodes"][episode["id"]]
                if metadata_episode["id"] == episode["id"]:
                    if not max(episode["created_at"], episode["updated_at"]) > max(
                        metadata_episode["created_at"], metadata_episode["updated_at"]
                    ):
                        # 更新がないエピソードはダウンロードをスキップ
                        episode["title"] = metadata_episode["title"]
                        new_metadata["episodes"][episode["id"]] = metadata_episode
                        metadata_images += metadata_episode["images"]
                        skipped_count += 1
                        print(
                            f'Download skipped (already up to date) ({i + 1}/{len(episodes)}): https://ncode.syosetu.com/{novel_id}/{episode["id"]}/'
                        )
                        continue
        print(
            f'Downloading ({i + 1}/{len(episodes)}): https://ncode.syosetu.com/{novel_id}/{episode["id"]}/'
        )
        episode_parser.feed(
            get(f'https://ncode.syosetu.com/{novel_id}/{episode["id"]}/')
        )
        downloaded_count += 1
        episode["title"] = episode_parser.title
        episode["paragraphs"] = episode_parser.paragraphs
        episode["fetched"] = True
        images += episode_parser.images
        new_metadata["episodes"][episode["id"]] = {
            "id": episode["id"],
            "title": episode["title"],
            "created_at": episode["created_at"],
            "updated_at": episode["updated_at"],
            "images": [
                {
                    "id": image["id"],
                    "name": image["name"],
                    "type": image["type"],
                }
                for image in episode_parser.images
            ],
        }
        episode_parser.reset()
        # 負荷かけないようにちょっと待つ
        time.sleep(1)

    print(f"Download is complete! (new: {downloaded_count}, skipped: {skipped_count})")

    with tempfile.NamedTemporaryFile(
        prefix=output, dir=os.getcwd(), delete=False
    ) as tmp_file:
        tmp_file_name = tmp_file.name
        with zipfile.ZipFile(
            tmp_file, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as zf_new:
            unique_images: List[MetadataImage] = []
            image_md5s = set()
            for image in images:
                if image["id"] not in image_md5s:
                    image_md5s.add(image["id"])
                    unique_images.append(image)
                    zf_new.writestr(f'src/image/{image["name"]}', image["data"])
            for episode in episodes:
                if episode["fetched"]:
                    zf_new.writestr(
                        f'src/text/{episode["id"]}.xhtml',
                        text(episode["title"], episode["paragraphs"]),
                    )
            if metadata:
                with zipfile.ZipFile(output, "r") as zf_old:
                    for metadata_image in metadata_images:
                        if metadata_image["id"] not in image_md5s:
                            image_md5s.add(metadata_image["id"])
                            unique_images.append(metadata_image)
                            with zf_old.open(
                                f'src/image/{metadata_image["name"]}'
                            ) as f:
                                zf_new.writestr(
                                    f'src/image/{metadata_image["name"]}', f.read()
                                )
                    for episode in episodes:
                        if not episode["fetched"]:
                            with zf_old.open(f'src/text/{episode["id"]}.xhtml') as f:
                                zf_new.writestr(
                                    f'src/text/{episode["id"]}.xhtml', f.read()
                                )
            zf_new.writestr("mimetype", "application/epub+zip")
            zf_new.writestr("META-INF/container.xml", container())
            zf_new.writestr("src/style.css", style())
            zf_new.writestr(
                "src/content.opf",
                content(title, author, timestamp, episodes, unique_images),
            )
            zf_new.writestr("src/navigation.xhtml", nav(chapters))
            zf_new.writestr("src/metadata.json", json.dumps(new_metadata))

    if os.path.exists(output):
        os.remove(output)
        os.rename(tmp_file_name, output)
        print(f"Updated {output}.")
    else:
        os.rename(tmp_file_name, output)
        print(f"Created {output}.")


if __name__ == "__main__":
    main()
