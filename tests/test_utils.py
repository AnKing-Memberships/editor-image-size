from src.editor_image_size.utils import (  # pylint: disable=import-error
    with_shrunken_images,
)


def test_with_shrunken_images():
    assert (
        with_shrunken_images('<img src="foo.jpg"/>')
        == '<img src="foo.jpg" data-editor-shrink="true"/>'
    )

    assert (
        with_shrunken_images('<img src="foo.jpg">')
        == '<img src="foo.jpg" data-editor-shrink="true">'
    )

    # with ">" in the src attribute
    assert (
        with_shrunken_images('<img src=">.jpg">')
        == '<img src=">.jpg" data-editor-shrink="true">'
    )

    # image tags with ">" in attributes other than src are ignored
    assert (
        with_shrunken_images('<img src="foo.jpg" class=">">')
        == '<img src="foo.jpg" class=">">'
    )
