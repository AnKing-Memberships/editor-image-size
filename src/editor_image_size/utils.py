import re
from typing import Optional

from anki.notes import Note


def shrink_images(
    note: Note,
) -> None:
    for ord, field in enumerate(note.fields):
        note.fields[ord] = with_shrunken_images(field)


def with_shrunken_images(html: str, img_name: Optional[str] = None) -> str:
    # if img_name is None all images are shrunk,
    # else only images with the given name

    if img_name is None:
        img_name = r'[^"]+'

    result = html
    for m in re.finditer(rf'<img [^>]*src="{img_name}"[^>]*>', html):
        if 'data-editor-shrink="true"' not in m.group(0):
            new_img_tag = m.group(0)[:-1] + ' data-editor-shrink="true">'
            result = result[: m.start()] + new_img_tag + result[m.end() :]

    return result
