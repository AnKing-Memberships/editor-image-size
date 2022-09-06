import re
import warnings

import bs4

# to make the tests work
try:
    from anki.notes import Note  # pylint: disable=unused-import
except:
    pass

# without this Anki sometimes shows MarkupResemblesLocatorWarnings issued by bs4
warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


def shrink_images(
    note: "Note",
) -> None:
    for ord, field in enumerate(note.fields):
        note.fields[ord] = with_shrunken_images(field)


def with_shrunken_images(html: str) -> str:
    # add data-editor-shrink attributes to all img tags that don't have it yet
    # img tags that have ">" signs in attributes other than the src are ignored
    # (this is a limitation due to using a regex and being careful not to break the html and
    #  Anki replaces ">" with "&gt;" in the editor anyway, but maybe not in all versions and situations)
    # this regex approach is used to not make formatting changes in the html when converting from html to soup to html.

    # img_file_names is used to make it more unlikely that the img regex matches something that it shouldn't
    soup = bs4.BeautifulSoup(html, "html.parser")
    img_file_names = list(
        set(
            img.get("src")
            for img in soup.find_all("img")
            if not img.get("data-editor-shrink")
            and all(
                ">" not in value or key == "src" for key, value in img.attrs.items()
            )
        )
    )
    if not img_file_names:
        return html

    file_names_re = "|".join(img_file_names)

    result = html

    # use reversed so that match positions don't shift after replacements
    for m in reversed(
        list(re.finditer(rf'<img [^>]*?src=[\'"]({file_names_re})[\'"][^>]*?>', result))
    ):
        if 'data-editor-shrink="true"' not in m.group(0):
            old_img_tag = m.group(0)
            if old_img_tag.endswith("/>"):
                new_img_tag = old_img_tag[:-2] + ' data-editor-shrink="true"/>'
            else:
                new_img_tag = old_img_tag[:-1] + ' data-editor-shrink="true">'
            result = result[: m.start()] + new_img_tag + result[m.end() :]

    return result
