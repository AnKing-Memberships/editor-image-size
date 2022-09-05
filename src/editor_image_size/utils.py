import json
import re
from typing import Optional

from anki.notes import Note
from aqt.editor import Editor


def shrink_images(
    note: Note,
) -> None:
    for ord, field in enumerate(note.fields):
        note.fields[ord] = with_shrunken_images(field)


def with_shrunken_images(html: str, img_name: Optional[str] = None) -> str:
    # if img_name is not None, only images with the given name are shrunk,
    # else all images

    if img_name is None:
        img_name = r'[^"]+'

    result = html
    for m in re.finditer(rf'<img [^>]*src="{img_name}"[^>]*>', html):
        if 'data-editor-shrink="true"' not in m.group(0):
            new_img_tag = m.group(0)[:-1] + ' data-editor-shrink="true">'
            result = result[: m.start()] + new_img_tag + result[m.end() :]

    return result


def overwrite_editor_field(editor: Editor, ord: int, content: str) -> None:
    editor.web.eval(
        f"""
        focusField({ord})
        document.execCommand('selectAll', false)
        document.execCommand('insertHTML', false, {json.dumps(content)})
        """
    )
