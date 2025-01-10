from typing import List, TypedDict


class Episode(TypedDict):
    id: str
    title: str
    paragraphs: List[str]


class Chapter(TypedDict):
    name: str
    episodes: List[Episode]


class Image(TypedDict):
    name: str
    id: str
    type: str
    data: bytes
