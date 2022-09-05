from anki.hooks import wrap
from aqt import mw
from aqt.editor import Editor

from .constants import ADDON_DIR_NAME
from .utils import with_shrunken_images


def setup_editor() -> None:
    def shrink_pasted_images(editor: Editor, html: str, internal: bool, _old) -> str:
        result = _old(editor, html, internal)

        if not mw.addonManager.getConfig(ADDON_DIR_NAME)["shrink_images_on_paste"]:
            return result

        result = with_shrunken_images(result)
        return result

    # tried to implement it using the editor_with_paste hook instead of monkey patching,
    # but this made it so that the undo history didn't work anymore
    Editor._pastePreFilter = wrap(  # pylint: disable=protected-access
        Editor._pastePreFilter,  # pylint: disable=protected-access
        shrink_pasted_images,
        "around",
    )
