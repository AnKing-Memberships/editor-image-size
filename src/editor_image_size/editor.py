import re

import bs4
from aqt import mw
from aqt.editor import Editor
from aqt.gui_hooks import editor_did_paste

from .constants import ADDON_DIR_NAME
from .utils import overwrite_editor_field


def on_editor_did_paste(
    editor: Editor,
    html: str,
    internal: bool,  # pylint: disable=unused-argument
    extended: bool,  # pylint: disable=unused-argument
) -> None:
    if not mw.addonManager.getConfig(ADDON_DIR_NAME)["shrink_images_on_paste"]:
        return

    soup = bs4.BeautifulSoup(html, "html.parser")
    imgs = soup.findAll("img")

    if not imgs:
        return

    imgs_to_shrink = [
        img.attrs["src"] for img in imgs if not img.attrs.get("data-editor-shrink")
    ]

    def run() -> None:
        field = editor.note.fields[editor.currentField]
        for img_name in imgs_to_shrink:
            field = re.sub(
                rf'(<img [^>]*src="{img_name}")',
                r"\1 data-editor-shrink=true",
                field,
            )

        # this makes it possible to undo the change from the html editor
        # it unfortunately doesn't work from the normal editor
        # there are discussions about reworking the undo system in the Anki repo
        overwrite_editor_field(editor, editor.currentField, field)

    editor.call_after_note_saved(lambda: run(), keepFocus=True)


def setup_editor() -> None:
    editor_did_paste.append(on_editor_did_paste)
