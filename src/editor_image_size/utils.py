import json
import re

from anki.notes import Note
from aqt.editor import Editor


def shrink_images(
    note: Note,
) -> None:
    for ord, field in enumerate(note.fields):
        field = re.sub(
            r'(<img [^>]*src="[^"]+")',
            r"\1 data-editor-shrink=true",
            field,
        )
        note.fields[ord] = field


def overwrite_editor_field(editor: Editor, ord: int, content: str) -> None:
    editor.web.eval(
        f"""
        focusField({ord})
        document.execCommand('selectAll', false)
        document.execCommand('insertHTML', false, {json.dumps(content)})
        """
    )
