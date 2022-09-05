import re
from typing import List, Optional

from anki.notes import Note


def shrink_images(note: Note, img_file_names: Optional[List[str]] = None) -> None:
    # shrinks images in note
    # if img_file_names is None, shrinks all images in note
    # if img_file_names is not None, shrinks only images with file names in img_file_names

    for ord, field in enumerate(note.fields):
        if img_file_names is not None:
            for file_name in img_file_names:
                if f'<img src="{file_name}"' in field:
                    field = re.sub(
                        rf'(<img [^>]*src="{file_name}")',
                        r"\1 data-editor-shrink=true",
                        field,
                    )
        else:
            field = re.sub(
                r'(<img [^>]*src="[^"]+")',
                r"\1 data-editor-shrink=true",
                field,
            )

        note.fields[ord] = field
