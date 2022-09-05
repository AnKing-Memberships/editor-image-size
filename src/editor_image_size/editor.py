import bs4
from aqt import mw
from aqt.editor import Editor
from aqt.gui_hooks import editor_did_paste

from .constants import ADDON_DIR_NAME
from .utils import shrink_images


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

    img_file_names = [img.attrs["src"] for img in imgs]

    def _run(editor: Editor) -> None:
        shrink_images(editor.note, img_file_names)
        editor.loadNoteKeepingFocus()

    editor.call_after_note_saved(lambda: _run(editor), keepFocus=True)


def setup_editor() -> None:
    editor_did_paste.append(on_editor_did_paste)
