from typing import Optional

from anki.notes import NoteId
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

    mw.taskman.with_progress(
        task=lambda: shrink_images_in_notes(browser.selected_notes()),
        on_done=lambda _: mw.update_undo_actions,
    )

    def shrink_images_in_currently_edited_note(editor: Editor) -> None:
        shrink_images(editor.note)
        editor.loadNoteKeepingFocus()

        mw.update_undo_actions()

    if (
        browser.editor
        and browser.editor.note
        and browser.editor.note.id in browser.selected_notes()
    ):
        browser.editor.call_after_note_saved(
            lambda: shrink_images_in_currently_edited_note(browser.editor),
            keepFocus=True,
        )


def shrink_images_in_notes(nids: list[NoteId]) -> None:
    undo_entry = mw.col.add_custom_undo_entry("Shrink images")
    for nid in nids:
        note = mw.col.get_note(nid)
        shrink_images(note)

        mw.col.update_note(note)
        mw.col.merge_undo_entries(undo_entry)


def setup_browser() -> None:
    browser_will_show_context_menu.append(on_browser_will_show_context_menu)
