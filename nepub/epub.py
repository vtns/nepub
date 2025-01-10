from typing import List, Tuple
import zipfile
from jinja2 import Environment, PackageLoader
from importlib import resources
from nepub.type import Chapter, Episode, Image

env = Environment(
    loader=PackageLoader("nepub"),
    # データ取得の際にエスケープ加工するので
    # ここではエスケープしない
    autoescape=False,
)
template_content = env.get_template("content.opf")
template_navigation = env.get_template("navigation.xhtml")
template_text = env.get_template("text.xhtml")


def content(
    title: str,
    author: str,
    created_at: str,
    episodes: List[Episode],
    images: List[Image],
):
    return template_content.render(
        {
            "title": title,
            "author": author,
            "created_at": created_at,
            "episodes": episodes,
            "images": images,
        }
    )


def nav(chapters: List[Chapter]):
    return template_navigation.render({"chapters": chapters})


def text(title: str, paragraphs: List[str]):
    return template_text.render({"title": title, "paragraphs": paragraphs})


def container():
    return resources.read_text("nepub.files", "container.xml")


def style():
    return resources.read_text("nepub.files", "style.css")


def compose(file_name: str, files: List[Tuple[str, str | bytes]]):
    with zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.writestr(
                file[0], file[1], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
            )
