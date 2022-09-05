from typing import Optional

from aqt import mw
from aqt.browser import Browser
from aqt.editor import Editor
from aqt.gui_hooks import browser_will_show_context_menu
from aqt.qt import QMenu
from aqt.utils import tr

from .utils import shrink_images


def on_browser_will_show_context_menu(browser: Browser, context_menu: QMenu) -> None:
    if browser.table.is_notes_mode():
        menu = context_menu
    else:
        notes_submenu: Optional[QMenu] = next(
            (
                menu  # type: ignore
                for menu in context_menu.findChildren(QMenu)
                if menu.title() == tr.qt_accel_notes()  # type: ignore
            ),
            None,
        )
        if notes_submenu is None:
            return
        menu = notes_submenu

    menu.addSeparator()
    menu.addAction(
        "Shrink images",
        lambda: on_shrink_images_action(browser),
    )


def on_shrink_images_action(browser: Browser):
    for nid in browser.selected_notes():
        note = mw.col.get_note(nid)
        shrink_images(note)
        note.flush()

    def _run(editor: Editor) -> None:
        shrink_images(editor.note)
        editor.loadNoteKeepingFocus()

    if (
        browser.editor
        and browser.editor.note
        and browser.editor.note.id in browser.selected_notes()
    ):
        browser.editor.call_after_note_saved(
            lambda: _run(browser.editor), keepFocus=True
        )


def setup_browser() -> None:
    browser_will_show_context_menu.append(on_browser_will_show_context_menu)
