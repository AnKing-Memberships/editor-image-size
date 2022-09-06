import os


def entry_point():
    from .browser import setup_browser
    from .editor import setup_editor

    setup_editor()
    setup_browser()


if not os.getenv("SKIP_INIT"):
    entry_point()
