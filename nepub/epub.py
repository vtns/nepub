from typing import List
from jinja2 import Environment, PackageLoader
from importlib import resources
from nepub.type import Chapter, Episode

env = Environment(
    loader=PackageLoader('nepub'),
    autoescape=True
)
template_content = env.get_template('content.opf')
template_navigation = env.get_template('navigation.xhtml')
template_text = env.get_template('text.xhtml')


def content(title: str, author: str, created_at: str, episodes: List[Episode]):
    return template_content.render({
        'title': title,
        'author': author,
        'created_at': created_at,
        'episodes': episodes
    })


def nav(chapters: List[Chapter]):
    return template_navigation.render({
        'chapters': chapters
    })


def text(title: str, paragraphs: List[str]):
    return template_text.render({
        'title': title,
        'paragraphs': paragraphs
    })


def container():
    return resources.read_text('nepub.files', 'container.xml')


def style():
    return resources.read_text('nepub.files', 'style.css')
